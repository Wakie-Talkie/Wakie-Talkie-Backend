from django.shortcuts import render, get_object_or_404, redirect
from .models import User, AI_User, Language
from .forms import UserForm, AI_UserForm, RecordingForm, VocabListForm
from rest_framework import generics
from .serializers import UserSerializer, AIUserSerializer,RecordingSerializer,VocabListSerializer,AudioFileSerializer, TranscriptionSerializer
from openai import OpenAI
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .models import User, AI_User, Recording, VocabList
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from . import serializers

import os
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
    OPENAI_API_KEY = "키값 적으세용"
    client = OpenAI(api_key=OPENAI_API_KEY)
    # STT (음성을 텍스트로 변환하는 함수)
    def stt_function(audio_file_path):
        client = OpenAI(api_key=OPENAI_API_KEY)
        # 오디오 파일을 열어서 텍스트로 변환하는 요청을 보냅니다.
        with open(audio_file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(file=audio_file, model="whisper-1")
            return transcription.text

    # GPT (대화를 생성하는 함수)
    def gpt_function(text, gpt_history):
        # OpenAI 클라이언트 초기화
        client = OpenAI(api_key=OPENAI_API_KEY)
        # 이전 대화 내용과 사용자의 설명을 포함하여 대화를 생성하는 요청을 보냅니다.
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=gpt_history + [
                {"role": "system", "content": ai_user_info.description},  # 시스템 메시지로 사용자 설명 추가
                {"role": "user", "content": text},  # 사용자가 입력한 텍스트 추가
            ],
        )
        # 대화 결과를 반환합니다.
        return response.choices[0].message.content, response.choices

    # TTS (텍스트를 음성으로 변환하는 함수)
    def tts_function(text, voice):
        # 음성 생성 요청을 보냅니다.
        response = client.audio.speech.create(
            model="tts-1",
            #voice=ai_user_info.nickname,  # 사용자의 닉네임을 음성으로 사용합니다.
            voice="alloy",
            input=text
        )
        # 생성된 음성을 반환합니다.
        #return response.choices[0].message.content

        #for test
        # API 응답을 파일로 저장합니다.
        file_name = "output_audio.mp3"
        with open(file_name, "wb") as audio_file:
            audio_file.write(response.content)

        # 저장된 파일을 읽어서 음성 데이터를 반환합니다.
        with open(file_name, "rb") as audio_file:
            audio_data = audio_file.read()

        # 파일을 삭제합니다.
        os.remove(file_name)

        return audio_data
    # 메인 로직
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
        serializer = AudioFileSerializer(data=request.data)
        if serializer.is_valid():
            audio_file = serializer.validated_data['audio_file']
            ai_user_id = request.user.id
            ai_user_info = AI_User.objects.get(id=ai_user_id)
            # STT, GPT, TTS 처리
            tts_output, gpt_history = sttgpttts(audio_file, ai_user_info, [])
            return Response({'transcription': tts_output})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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