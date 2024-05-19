from django.shortcuts import render, get_object_or_404, redirect
from .models import User, AI_User, Alarm, Language
from .forms import UserForm, AI_UserForm, AlarmForm
from rest_framework import generics
from .models import User, AI_User
from .serializers import UserSerializer, AIUserSerializer
from django.http import JsonResponse
from openai import OpenAI
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
<<<<<<< Updated upstream
=======
from django.http import JsonResponse
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse, FileResponse, StreamingHttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from . import serializers
>>>>>>> Stashed changes

# 사용자 리스트 보기
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

# 사용자 추가
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'user_create.html', {'form': form})

# 사용자 상세 정보 보기
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'user_detail.html', {'user': user})

# 사용자 수정
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_detail', pk=user.pk)
    else:
        form = UserForm(instance=user)
    return render(request, 'user_update.html', {'form': form})

# 사용자 삭제
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'user_delete_confirm.html', {'user': user})

# AI 사용자 리스트 보기
def ai_user_list(request):
    ai_users = AI_User.objects.all()
    return render(request, 'ai_user_list.html', {'ai_users': ai_users})

# AI 사용자 추가
def ai_user_create(request):
    if request.method == 'POST':
        form = AI_UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ai_user_list')
    else:
        form = AI_UserForm()
    return render(request, 'ai_user_create.html', {'form': form})

# AI 사용자 상세 정보 보기
def ai_user_detail(request, pk):
    ai_user = get_object_or_404(AI_User, pk=pk)
    return render(request, 'ai_user_detail.html', {'ai_user': ai_user})

# AI 사용자 수정
def ai_user_update(request, pk):
    ai_user = get_object_or_404(AI_User, pk=pk)
    if request.method == 'POST':
        form = AI_UserForm(request.POST, request.FILES, instance=ai_user)
        if form.is_valid():
            form.save()
            return redirect('ai_user_detail', pk=ai_user.pk)
    else:
        form = AI_UserForm(instance=ai_user)
    return render(request, 'ai_user_update.html', {'form': form})

# AI 사용자 삭제
def ai_user_delete(request, pk):
    ai_user = get_object_or_404(AI_User, pk=pk)
    if request.method == 'POST':
        ai_user.delete()
        return redirect('ai_user_list')
    return render(request, 'ai_user_delete_confirm.html', {'ai_user': ai_user})

#serializer사용 api view

class UserListAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AIUserListAPIView(APIView):
    def get(self, request):
        ai_users = AI_User.objects.all()
        serializer = AIUserSerializer(ai_users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AIUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# CREATE(Create)
class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class AIUserCreateAPIView(generics.CreateAPIView):
    queryset = AI_User.objects.all()
    serializer_class = AIUserSerializer

<<<<<<< Updated upstream
# UPDATE(Update)
class UserUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class AIUserUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = AI_User.objects.all()
    serializer_class = AIUserSerializer

# DELETE(Delete)
class UserDeleteAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class AIUserDeleteAPIView(generics.DestroyAPIView):
    queryset = AI_User.objects.all()
    serializer_class = AIUserSerializer
=======
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

#STT, GPT, TTS, 처리 함수
# STT, GPT, TTS 기능을 구현한 함수
def sttgpttts(audio_file_path, ai_user_info, gpt_history):
    OPENAI_API_KEY = "yourkey"

    client = OpenAI(api_key=OPENAI_API_KEY)

    # STT (음성을 텍스트로 변환하는 함수)
    def stt_function(audio_file_path):
        with open(audio_file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(file=audio_file, model="whisper-1")
        return transcription.text

    # GPT (대화를 생성하는 함수)
    def gpt_function(text, gpt_history):
        response = client.chat.completions.create(
            model="gpt-4",
            messages=gpt_history + [
                {"role": "system", "content": ai_user_info.description},
                {"role": "user", "content": text},
            ],
        )
        return response.choices[0].message.content, response.choices

    # TTS (텍스트를 음성으로 변환하는 함수)
    def tts_function(text):
        response = client.audio.speech.create(
            model="tts-1",
            voice='alloy',
            input=text
        )
        return response

    # 1. 음성 파일을 텍스트로 변환
    transcription = stt_function(audio_file_path)
    # 2. GPT를 사용하여 대화 생성
    gpt_output, gpt_history = gpt_function(transcription, gpt_history)
    # 3. 생성된 대화를 문장 단위로 나누기
    sentences = gpt_output.split('.')
    return sentences, gpt_history, tts_function

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
            try:
                ai_user_info = AI_User.objects.get(id=ai_user_id)
            except AI_User.DoesNotExist:
                return Response({'error': 'AI_User matching the provided ID does not exist.'},
                                status=status.HTTP_404_NOT_FOUND)

            original_path = audio_file.recorded_audio_file.path
            base, ext = os.path.splitext(original_path)
            new_path = base + '.mp3'
            os.rename(original_path, new_path)
            audio_file.recorded_audio_file.name = new_path[len(settings.MEDIA_ROOT) + 1:]
            audio_file.save()

            # STT, GPT, TTS 처리
            sentences, gpt_history, tts_function = sttgpttts(new_path, ai_user_info, [])

            # 생성된 음성 파일을 순차적으로 스트리밍하는 함수
            def generate():
                for sentence in sentences:
                    if sentence.strip():
                        tts_response = tts_function(sentence.strip() + '.')
                        yield tts_response.content

            response = StreamingHttpResponse(generate(), content_type='audio/mpeg')
            response['Content-Disposition'] = 'attachment; filename="output.mp3"'
            return response
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
>>>>>>> Stashed changes
