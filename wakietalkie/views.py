from django.shortcuts import render, get_object_or_404, redirect

from djangoProject6 import settings
from .models import *
from .forms import *
from rest_framework import generics
from .serializers import *
from openai import OpenAI
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from . import serializers

import os
import tempfile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import FileSystemStorage
import time

def handle_uploaded_file(uploaded_file: InMemoryUploadedFile):
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        for chunk in uploaded_file.chunks():
            tmp_file.write(chunk)
        return tmp_file.name  # 임시 파일 경로 반환


def index(request):
    return HttpResponse("Welcome to my Django Project!")

# Helper function to serialize list of objects
def serialize_list(objects, serializer_class):
    serializer = serializer_class(objects, many=True)
    return serializer.data

# Helper function to serialize single object
def serialize_object(obj, serializer_class):
    serializer = serializer_class(obj)
    return serializer.data

# User List and Create View
class UserListCreateAPIView(APIView):
    def get(self, request, format=None):
        users = User.objects.all()
        return Response(serialize_list(users, UserSerializer))

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Detail, Update and Delete View
class UserDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(User, pk=pk)

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        return Response(serialize_object(user, UserSerializer))

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LanguageListCreateAPIView(APIView):
    def get(self, request, format=None):
        languages = Language.objects.all()
        return Response(serialize_list(languages, LanguageSerializer))
    def post(self, request, format=None):
        serializer = LanguageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# AI User List and Create View
class AIUserListCreateAPIView(APIView):
    def get(self, request, format=None):
        ai_users = AI_User.objects.all()
        return Response(serialize_list(ai_users, AIUserSerializer))

    def post(self, request, format=None):
        serializer = AIUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# AI User Detail, Update and Delete View
class AIUserDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(AI_User, pk=pk)

    def get(self, request, pk, format=None):
        ai_user = self.get_object(pk)
        return Response(serialize_object(ai_user, AIUserSerializer))

    def put(self, request, pk, format=None):
        ai_user = self.get_object(pk)
        serializer = AIUserSerializer(ai_user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        ai_user = self.get_object(pk)
        ai_user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#Language로 ai-user list
class AIUserListByLanguageAPIView(generics.ListAPIView):
    serializer_class = AIUserSerializer

    def get_queryset(self):
        language_id = self.kwargs.get('language_id')  # URL에서 언어 ID를 가져옵니다.
        if language_id is not None:
            return AI_User.objects.filter(language_id=language_id)
        else:
            return AI_User.objects.all()

# Recording List and Create View
class RecordingListCreateAPIView(APIView):
    def get(self, request, format=None):
        recordings = Recording.objects.all()
        return Response(serialize_list(recordings, RecordingSerializer))

    def post(self, request, format=None):
        serializer = RecordingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Recording Detail, Update and Delete View
class RecordingDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Recording, pk=pk)

    def get(self, request, pk, format=None):
        recording = self.get_object(pk)
        return Response(serialize_object(recording, RecordingSerializer))

    def put(self, request, pk, format=None):
        recording = self.get_object(pk)
        serializer = RecordingSerializer(recording, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        recording = self.get_object(pk)
        recording.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Recording List By User View
class RecordingListByUserView(APIView):
    def get(self, request, user_id, format=None):
        recordings = Recording.objects.filter(user_id=user_id)
        serializer = RecordingSerializer(recordings, many=True)
        return Response(serializer.data)

    def post(self, request, user_id, format=None):
        request.data['user_id'] = user_id  # Ensure user_id is set before saving
        serializer = RecordingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# VocabList List and Create View
class VocabListListCreateAPIView(APIView):
    def get(self, request, format=None):
        vocab_lists = VocabList.objects.all()
        return Response(serialize_list(vocab_lists, VocabListSerializer))

    def post(self, request, format=None):
        serializer = VocabListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# VocabList Detail, Update and Delete View
class VocabListDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(VocabList, pk=pk)

    def get(self, request, pk, format=None):
        vocab_list = self.get_object(pk)
        return Response(serialize_object(vocab_list, VocabListSerializer))

    def put(self, request, pk, format=None):
        vocab_list = self.get_object(pk)
        serializer = VocabListSerializer(vocab_list, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        vocab_list = self.get_object(pk)
        vocab_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Latest VocabList View
class LatestVocabListView(APIView):
    def get(self, request, format=None):
        latest_vocab_list = VocabList.objects.latest('created_at')
        serializer = VocabListSerializer(latest_vocab_list)
        return Response(serializer.data)

# VocabList View
class VocabListView(APIView):
    def get(self, request, format=None):
        vocab_lists = VocabList.objects.all()
        serializer = VocabListSerializer(vocab_lists, many=True)
        return Response(serializer.data)


#STT,GPT,TTS에 관한 view
def sttgpttts(audio_file_path, ai_user_info, gpt_history):
    OPENAI_API_KEY = "key"

    client = OpenAI(api_key=OPENAI_API_KEY)
    # STT (음성을 텍스트로 변환하는 함수)
    def stt_function(audio_file_path):
        client = OpenAI(api_key=OPENAI_API_KEY)
        # file_bytes = audio_file_data.read()
        # 오디오 파일을 열어서 텍스트로 변환하는 요청을 보냅니다.
        start_time = time.time()
        with open(audio_file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(file=audio_file, model="whisper-1")
            end_time = time.time()
            # 걸린 시간 계산
            elapsed_time = end_time - start_time

            print(f"stt 작업에 걸린 시간: {elapsed_time} 초")
        return transcription.text

    # GPT (대화를 생성하는 함수)
    def gpt_function(text, gpt_history):
        # OpenAI 클라이언트 초기화
        client = OpenAI(api_key=OPENAI_API_KEY)
        # 이전 대화 내용과 사용자의 설명을 포함하여 대화를 생성하는 요청을 보냅니다.
        start_time = time.time()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=gpt_history + [
                {"role": "system", "content": ai_user_info.description},  # 시스템 메시지로 사용자 설명 추가
                {"role": "user", "content": text},  # 사용자가 입력한 텍스트 추가
            ],
        )
        end_time = time.time()
        # 걸린 시간 계산
        elapsed_time = end_time - start_time
        print(f"gpt 작업에 걸린 시간: {elapsed_time} 초")
        # 대화 결과를 반환합니다.
        return response.choices[0].message.content, response.choices

    # TTS (텍스트를 음성으로 변환하는 함수)
    def tts_function(text, voice):
        # 음성 생성 요청을 보냅니다.
        start_time = time.time()
        response = client.audio.speech.create(
            model="tts-1",
            #voice=ai_user_info.nickname,  # 사용자의 닉네임을 음성으로 사용합니다.
            voice=voice,
            input=text
        )
        end_time = time.time()

        # 걸린 시간 계산
        elapsed_time = end_time - start_time
        print(f"tts api 작업에 걸린 시간: {elapsed_time} 초")
        # 생성된 음성을 반환합니다.
        #return response.choices[0].message.content
        start_time = time.time()
        media_root = settings.MEDIA_ROOT
        file_name = "output_audio.mp3"
        # 파일의 전체 경로를 생성합니다.
        file_path = os.path.join(media_root, file_name)

        # FileSystemStorage 인스턴스를 생성합니다.
        fs = FileSystemStorage(location=media_root)

        response.stream_to_file(file_path)

        # 끝나는 시간 기록
        end_time = time.time()

        # 걸린 시간 계산
        elapsed_time = end_time - start_time
        print(f"tts 작업에 걸린 시간: {elapsed_time} 초")
        # 파일을 저장합니다.
        # with fs.open(file_name, 'wb') as f:
        #     f.write(file_content)
        #
        print(fs.url(file_name))
        return fs.url(file_name)

    # 1. 음성 파일을 텍스트로 변환합니다.
    transcription = stt_function(audio_file_path)
    # 2. GPT를 사용하여 대화를 생성합니다.
    gpt_output, gpt_history = gpt_function(transcription, gpt_history)
    # 3. 생성된 대화를 음성으로 변환합니다.
    tts_output = tts_function(gpt_output, ai_user_info.nickname)  # 사용자의 언어로 설정

    # 음성 결과와 GPT 대화 기록을 반환합니다.
    return tts_output, gpt_history


class AudioFileUpload(APIView):
    def post(self, request):
        data = request.data.copy()

        # 기본값 설정
        if 'calling_time' not in data:
            data['calling_time'] = 'unknown'
        if 'converted_text_file' not in data:
            data['converted_text_file'] = 'No transcription available'
        if 'language' not in data:
            data['language'] = 1  # 기본 언어 설정

        file_serializer = AudioFileSerializer(data=data)
        if file_serializer.is_valid():
            audio_file = file_serializer.save()

            ai_user_id = audio_file.ai_partner_id
            print(f"ai_user_id: {ai_user_id}")  # 디버깅 출력

            try:
                ai_user_info = AI_User.objects.get(id=ai_user_id)
            except AI_User.DoesNotExist:
                return Response({'error': 'AI_User matching the provided ID does not exist.'},
                                status=status.HTTP_404_NOT_FOUND)

            start_time = time.time()
            original_path = audio_file.recorded_audio_file.path
            base, ext = os.path.splitext(original_path)
            new_path = base + '.mp3'
            os.rename(original_path,new_path)
            print(new_path)
            audio_file.recorded_audio_file.name = new_path[len(settings.MEDIA_ROOT) + 1:]
            audio_file.save()
            end_time = time.time()

            # 걸린 시간 계산
            elapsed_time = end_time - start_time
            print(f"파일 post 받은 거 저장 작업에 걸린 시간: {elapsed_time} 초")
            print(audio_file.recorded_audio_file.name)
            # audio_file = serializer.validated_data['recorded_audio_file']

            # STT, GPT, TTS 처리
            tts_output, gpt_history = sttgpttts(new_path, ai_user_info, [])

            return Response({'transcription': tts_output})
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TranscriptionRetrieve(APIView):
    def get(self, request):
        # STT, GPT, TTS 처리
        tts_output, _ = sttgpttts(None, None, [])
        return Response({'transcription': tts_output})

class SttGptTtsResponse(APIView):
    def get(self, request):
        # STT, GPT, TTS 처리
        tts_output, _ = sttgpttts(None, None, [])
        return Response({'transcription': tts_output})


class TtsResponse(APIView):
    def get(self, request):
        # STT, GPT, TTS 처리
        tts_output, gpt_history = sttgpttts(None, None, [])


class ConversationScriptAPIView(APIView):
    def get(self, request):
        # STT, GPT, TTS 처리
        _, gpt_history = sttgpttts(None, None, [])

        # 전체 대화 스크립트 생성
        script = [{'user': item['user'], 'ai': item['ai']} for item in gpt_history]

        # 전체 대화 스크립트 반환
        return Response({'conversation_script': script})

#전화 시작과 끝
from datetime import datetime

def handle_call_start(start_time, ai_user_id):
    # 전화가 시작된 시간과 전화를 한 AI 사용자의 ID를 기록하여 데이터베이스에 저장합니다.
    CallRecord.objects.create(start_time=start_time, ai_user_id=ai_user_id)

class CallStartAPIView(APIView):
    def post(self, request):
        # 전화가 시작되는 시간 기록
        start_time = datetime.now()

        # 전화를 시작한 AI 사용자의 정보 가져오기
        ai_user_id = request.data.get('ai_user_id')
        ai_user = AI_User.objects.get(id=ai_user_id)

        # 전화가 시작됨을 처리하는 코드 추가
        handle_call_start(start_time, ai_user_id)

        # 통화 시작 시간과 AI 사용자 정보를 반환
        response_data = {
            'start_time': start_time,
            'caller': ai_user.nickname,
            'language': ai_user.language.name
        }
        return Response(response_data, status=status.HTTP_200_OK)


class CallEndAPIView(APIView):
    def post(self, request):
        # 통화가 종료된 시간 기록
        end_time = datetime.now()

        # 통화 시작 시간 가져오기
        start_time_str = request.data.get('start_time')
        start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S.%f')

        # 통화의 기간 계산 (종료 시간 - 시작 시간)
        duration = end_time - start_time

        # 전화를 종료한 AI 사용자의 정보 가져오기
        ai_user_id = request.data.get('ai_user_id')
        ai_user = AI_User.objects.get(id=ai_user_id)

        # 전화가 종료됨을 알리는 작업 수행
        # 여기에 통화가 종료됨을 처리하는 코드를 추가합니다.

        # 통화 종료 시간과 AI 사용자 정보, 통화 기간을 반환
        response_data = {
            'end_time': end_time,
            'caller': ai_user.nickname,
            'language': ai_user.language.name,
            'duration': duration.total_seconds()  # 기간을 초 단위로 변환하여 반환
            # 이전에 만든 전체 대화 텍스트와 오디오에 접근하여 추가 정보를 가져옵니다.
            # 'conversation_text_url': 'URL_TO_CONVERSATION_TEXT',
            # 'conversation_audio_url': 'URL_TO_CONVERSATION_AUDIO'
        }
        # 전화 종료 시 데이터베이스에 기록
        CallRecord.objects.create(start_time=start_time, end_time=end_time, ai_user=ai_user)

        return Response(response_data, status=status.HTTP_200_OK)

# 통화 정보 및 대화 내용에 접근 가능한 API
class CallInfoAPIView(APIView):
    def post(self, request):
        # 전화 종료 정보 가져오기
        end_time_str = request.data.get('end_time')
        end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S.%f')

        # 전화 시작 시간 가져오기
        start_time_str = request.data.get('start_time')
        start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S.%f')

        # 통화의 기간 계산 (종료 시간 - 시작 시간)
        duration = end_time - start_time

        # 전화를 한 AI 사용자의 정보 가져오기
        ai_user_id = request.data.get('ai_user_id')
        ai_user = AI_User.objects.get(id=ai_user_id)

        # 통화 정보 및 대화 내용 가져오기
        call_info = {
            'caller': ai_user.nickname,
            'duration': duration.total_seconds(),  # 통화 기간을 초 단위로 변환하여 반환
            'language': ai_user.language.name,
            # 이전에 만든 전체 대화 텍스트와 오디오에 접근하여 추가 정보를 가져옵니다.
            'conversation_text_url': 'URL_TO_CONVERSATION_TEXT',
            'conversation_audio_url': 'URL_TO_CONVERSATION_AUDIO'
        }

        return Response(call_info, status=status.HTTP_200_OK)
