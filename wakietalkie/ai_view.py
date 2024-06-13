from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.parsers import FormParser, MultiPartParser
import requests
from .serializers import *

from wakietalkie.models import AI_User
from wakietalkie.serializers import AIUserSerializer
from django.http import FileResponse
from django.shortcuts import get_object_or_404
import os
from openai import OpenAI
import time
from pydub import AudioSegment

# Helper function to serialize list of objects
def serialize_list(objects, serializer_class):
    serializer = serializer_class(objects, many=True)
    return serializer.data

# Helper function to serialize single object
def serialize_object(obj, serializer_class):
    serializer = serializer_class(obj)
    return serializer.data
def get_sample_voice(ai_user_info):
    sample_dir = "audio-storage/samples/"
    file_name = f"{ai_user_info.nickname}"
    os.makedirs(os.path.dirname(sample_dir), exist_ok=True)
    OPENAI_API_KEY = "key"
    client = OpenAI(api_key=OPENAI_API_KEY)

    def tts_function(text, voice):
        # 음성 생성 요청을 보냅니다.
        start_time = time.time()
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )
        end_time = time.time()

        # 걸린 시간 계산
        elapsed_time = end_time - start_time
        print(f"tts api 작업에 걸린 시간: {elapsed_time} 초")
        start_time = time.time()
        mp3_file_name = f"{file_name}.mp3"
        wav_file_name=f"{file_name}.wav"

        # 파일의 전체 경로를 생성합니다.
        file_path = os.path.join(sample_dir, mp3_file_name)
        response.stream_to_file(file_path)

        sound = AudioSegment.from_mp3(file_path)
        wav_file_path = os.path.join(sample_dir, wav_file_name)
        sound.export(wav_file_path, format="wav")
        # 끝나는 시간 기록
        end_time = time.time()

        # 걸린 시간 계산
        elapsed_time = end_time - start_time
        print(f"tts 작업에 걸린 시간: {elapsed_time} 초")

        if os.path.exists(file_path):
            os.remove(file_path)
        return wav_file_path
    def custom_tts_function(text, voice, language):
        # 음성 생성 요청을 보냅니다.
        start_time = time.time()
        # print(f"voice {voice}, language {language} text {text}")
        response = requests.post(
           # 'http://ec2-43-200-46-197.ap-northeast-2.compute.amazonaws.com:5001/tts/',
            'http://127.0.0.1:5001/tts/',
           json={'voice': voice, 'language': language.name, 'text': text}
        )
        if response.status_code == 200:
            audio_data = response.content
            end_time = time.time()

            # 걸린 시간 계산
            elapsed_time = end_time - start_time
            print(f"tts api 작업에 걸린 시간: {elapsed_time} 초")
            start_time = time.time()
            wav_file_name = f"{file_name}.wav"

            # 파일의 전체 경로를 생성합니다.
            file_path = os.path.join(sample_dir, wav_file_name)

            with open(file_path, 'wb') as audio_file:
                audio_file.write(audio_data)

            # 끝나는 시간 기록
            end_time = time.time()

            # 걸린 시간 계산
            elapsed_time = end_time - start_time
            print(f"tts 작업에 걸린 시간: {elapsed_time} 초")

            return file_path
        else:
            return Response({'error': 'Failed to generate speech'}, status.resopnse_code)

    if os.path.exists(f"{sample_dir}{file_name}.wav"):
        return f"{sample_dir}{file_name}.wav"
    else:
        if ai_user_info.ai_type == "openai":
            file_output_path = tts_function(ai_user_info.description, ai_user_info.nickname)
            return file_output_path
        else:
            file_output_path = custom_tts_function(ai_user_info.description, ai_user_info.nickname, ai_user_info.language)
            return file_output_path

class AISampleAudio(APIView):
    def get_object(self, pk):
        return get_object_or_404(AI_User, pk=pk)
    def get(self, request, pk, format=None):
        ai_user_info = self.get_object(pk)
        sample_output_path = get_sample_voice(ai_user_info)
        response = FileResponse(open(sample_output_path, 'rb'), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="output.wav"'
        return response
    def post(self, request):
        ai_user_id = request.data.get('ai_partner_id')

        try:
            ai_user_info = AI_User.objects.get(id=ai_user_id)
        except AI_User.DoesNotExist:
            return Response({'error': 'AI_User matching the provided ID does not exist.'},
                            status=status.HTTP_404_NOT_FOUND)
        sample_output_path = get_sample_voice(ai_user_info)
        response = FileResponse(open(sample_output_path, 'rb'), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="output.wav"'
        return response


# AI User List and Create View
class AIUserListCreateAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    def get_serializer_context(self):
        return {'request': self.request}

    def get(self, request, format=None):
        ai_users = AI_User.objects.all()
        context = self.get_serializer_context()
        serializer = AIUserSerializer(ai_users, many=True, context=context)
        return Response(serializer.data)

    def post(self, request, format=None):
        context = self.get_serializer_context()
        serializer = AIUserSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AIVoiceTransfer(APIView):
    def post(self, request, format=None):
        file = request.FILES['ai_voice_file']
        ai_name = request.data.get('ai_name')

        if not file:
            return Response({'error': 'no file'},status=status.HTTP_400_BAD_REQUEST)
        files = {'file': (ai_name, file.read(), file.content_type)}
        # response = requests.post('http://ec2-43-200-46-197.ap-northeast-2.compute.amazonaws.com:5001/upload-ai-voice/', files=files)
        response = requests.post('http://127.0.0.1:5001/upload-ai-voice/', files=files)
        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Failed to upload audio'}, status=response.status_code)


# AI User Detail, Update and Delete View
class AIUserDetailAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    def get_object(self, pk):
        return get_object_or_404(AI_User, pk=pk)

    def get_serializer_context(self):
        return {'request': self.request}

    def get(self, request, pk, format=None):
        ai_user = self.get_object(pk)
        context = self.get_serializer_context()
        serializer = AIUserSerializer(ai_user, context=context)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        ai_user = self.get_object(pk)
        context = self.get_serializer_context()
        serializer = AIUserSerializer(ai_user, data=request.data, partial=True, context=context)
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

