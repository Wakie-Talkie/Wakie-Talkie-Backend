from django.shortcuts import render, get_object_or_404, redirect

from djangoProject6 import settings
from djangoProject6.settings import MEDIA_URL
from .models import *
from .forms import *
from rest_framework import generics
from .serializers import *
from openai import OpenAI
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from django.http import JsonResponse
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse, FileResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from . import serializers
from datetime import datetime, date

import os
from mutagen import File
import time
from pydub import AudioSegment


conversation_history = []
store_url = ''
conversation_index = 1
recording_index = 1

def createVocabs(vocab_history_path):
    OPENAI_API_KEY = "key"

    client = OpenAI(api_key=OPENAI_API_KEY)
    with open(vocab_history_path, 'r', encoding='utf-8') as file:
        file_contents = file.read()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
             "content": "give me five json list format output only in [{\"word\":\"word1 from the conversation\",\"korean meaning\":\"korean meaning of the word1\",\"antonym\":\"antonym of the word1\",\"synonym\":\"synonym of the word1\",\"sentence\":\"example sentence using the word1\"},{\"word':'word2 from the conversation\",\"korean meaning\":\"korean meaning of the word2\",\"antonym\":\"antonym of the word2\",\"synonym\":\"synonym of the word2\",\"sentence\":\"example sentence using the word2\"},...] format that is useful in daily conversation from the incoming text"},
            {"role": "user",
             "content": file_contents}
        ],
    )
    # print(response.choices[0].message.content)
    return response.choices[0].message.content

def sttgpttts(audio_file_path, ai_user_info):
    OPENAI_API_KEY = "key"

    client = OpenAI(api_key=OPENAI_API_KEY)
    # STT (음성을 텍스트로 변환하는 함수)
    def stt_function(audio_file_path, language):
        # 오디오 파일을 열어서 텍스트로 변환하는 요청을 보냅니다.
        start_time = time.time()
        with open(audio_file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(file=audio_file, model="whisper-1", language=language)
            end_time = time.time()
            # 걸린 시간 계산
            elapsed_time = end_time - start_time

            print(f"stt 작업에 걸린 시간: {elapsed_time} 초")
            print(transcription.text)
        return transcription.text

    # GPT (대화를 생성하는 함수)
    def gpt_function(text):
        global conversation_history
        conversation_history.append({"role": "user", "content": text})
        start_time = time.time()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=conversation_history,
        )
        end_time = time.time()
        # 걸린 시간 계산
        elapsed_time = end_time - start_time
        print(f"gpt 작업에 걸린 시간: {elapsed_time} 초")
        conversation_history.append({"role": "assistant", "content": response.choices[0].message.content})
        print(response.choices[0].message.content)
        # 대화 결과를 반환합니다.
        return response.choices[0].message.content, conversation_history

    # TTS (텍스트를 음성으로 변환하는 함수)
    def tts_function(text, voice):
        global conversation_index
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
        file_name = f"ai{conversation_index}.mp3"
        wav_file_name=f"ai{conversation_index}.wav"
        conversation_index+=1

        # 파일의 전체 경로를 생성합니다.
        file_path = os.path.join(store_url, file_name)
        response.stream_to_file(file_path)

        sound = AudioSegment.from_mp3(file_path)
        wav_file_path = os.path.join(store_url, wav_file_name)
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
        global conversation_index
        # 음성 생성 요청을 보냅니다.
        start_time = time.time()
        print(f"voice {voice}, language {language} text {text}")
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
            file_name = f"ai{conversation_index}.wav"
            conversation_index += 1

            # 파일의 전체 경로를 생성합니다.
            file_path = os.path.join(store_url, file_name)

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

    transcription = stt_function(audio_file_path, ai_user_info.language)
    print(f"language : {ai_user_info.language}\n")
    print(f"lang type: {type(ai_user_info.language)}")
    print(f"nick type: {type(ai_user_info.language)}")
    gpt_output, file_content = gpt_function(transcription)
    print(f"type?? : {ai_user_info.ai_type}\n")
    if ai_user_info.ai_type == "openai":
        tts_output_path = tts_function(gpt_output, ai_user_info.nickname)
        return tts_output_path, file_content
    else:
        tts_output_path = custom_tts_function(gpt_output, ai_user_info.nickname, ai_user_info.language)
        return tts_output_path, file_content

class AudioFileUpload(APIView):
    def post(self, request):
        global store_url
        global conversation_index
        audio_file = request.FILES['recorded_audio_file']
        ai_user_id = request.data.get('ai_partner_id')

        try:
            ai_user_info = AI_User.objects.get(id=ai_user_id)
            print(ai_user_info.nickname)
            print(ai_user_info.language)

            print(ai_user_info.ai_type)
            # language_info = Language.objects.get(id=ai_user_info.language)
            # print(language_info)
        except AI_User.DoesNotExist:
            return Response({'error': 'AI_User matching the provided ID does not exist.'},
                            status=status.HTTP_404_NOT_FOUND)

        start_time = time.time()
        file_name = "user" + str(conversation_index) + ".wav"
        audio_file_path = os.path.join(store_url, file_name)
        with open(audio_file_path, 'wb+') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)

        end_time = time.time()
        # 걸린 시간 계산
        elapsed_time = end_time - start_time
        print(f"파일 post 받은 거 저장 작업에 걸린 시간: {elapsed_time} 초")
        # STT, GPT, TTS 처리
        tts_output_path, file_content = sttgpttts(audio_file_path, ai_user_info)
        response = FileResponse(open(tts_output_path, 'rb'), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="output.mp3"'
        return response
def resetRecordingSetting(ai_user_id, user_id):
    global recording_index
    global conversation_history
    global store_url
    current_date = date.today()
    # Format the date as a string in YYYY-mm-dd format
    formatted_date = current_date.strftime('%Y-%m-%d')
    # print(f"data?? {formatted_date}")
    store_url = "audio-storage/recordings/" + str(user_id) + "/" + str(ai_user_id) + "/" + formatted_date + "/send_call" + str(recording_index)+"/"
    print(f"store url : {store_url}\n")
    # print(f"recording index : {recording_index}")

    os.makedirs(os.path.dirname(store_url), exist_ok=True)

    conversation_history.clear()
    conversation_history.append({"role": "system", "content": "give me three or less short sentences"})
    # print(f"at call start! {conversation_history}")
    return conversation_history
class CallStartAPIView(APIView):
    def post(self, request):
        history = resetRecordingSetting(request.data.get('ai_partner_id'), request.data.get('user_id'))
        response_data = {
            'start_time': history
        }
        return Response(response_data, status=status.HTTP_200_OK)
def get_audio_runtime(file_path):
    audio = File(file_path)
    if audio is None or not hasattr(audio.info, 'length'):
        return "00:00"

    duration = int(audio.info.length)
    minutes, seconds = divmod(duration, 60)
    return f"{minutes:02}:{seconds:02}"

def merge_wav_files(input_files, output_file):
    # Create an empty AudioSegment
    combined = AudioSegment.empty()

    # Iterate over the list of input files and concatenate them
    for file in input_files:
        audio_path = os.path.join(store_url, file)
        audio = AudioSegment.from_wav(audio_path)
        combined += audio

    # Export the combined AudioSegment to a new file
    combined.export(output_file, format="wav")

def mergeRecordings():
    global store_url
    global recording_index
    global conversation_index
    global conversation_history

    audio_file_name = "combined_recording.wav"
    audio_output_path = os.path.join(store_url, audio_file_name)

    # List all audio files in the directory
    user_files = [f for f in os.listdir(store_url) if f.startswith('user')]
    ai_files = [f for f in os.listdir(store_url) if f.startswith('ai')]

    print(user_files)
    print(ai_files)
    # Sort each list based on the numeric part
    user_files.sort(key=lambda x: int(x[4:].split('.')[0]))
    ai_files.sort(key=lambda x: int(x[2:].split('.')[0]))

    # Interleave the two lists
    sorted_files = []
    for user, ai in zip(user_files, ai_files):
        sorted_files.append(user)
        sorted_files.append(ai)

    print(sorted_files)
    merge_wav_files(sorted_files, audio_output_path)

    # with open(audio_output_path, 'wb') as outfile:
    #     for file_name in sorted_files:
    #         file_path = os.path.join(store_url, file_name)
    #         with open(file_path, 'rb') as infile:
    #             outfile.write(infile.read())

    for file_name in sorted_files:
        file_path = os.path.join(store_url, file_name)
        os.remove(file_path)

    text_file_name = "combined_recording.txt"
    text_output_path = os.path.join(store_url, text_file_name)

    with open(text_output_path, 'w') as file:
        for history in conversation_history:
            for key, value in history.items():
                file.write(f"{key}: {value}\n")
            file.write("\n")  # Add a blank line between entries

    text_file_name = "vocab_history.txt"
    vocab_text_path = os.path.join(store_url, text_file_name)
    flag = False

    with open(vocab_text_path, 'w') as file:
        for history in conversation_history:
            for key, value in history.items():
                if flag:
                    file.write(f"{value} ")
                if value == "assistant":
                    flag =True
                else:
                    flag = False

    # initialize index
    recording_index += 1
    conversation_index = 1
    return audio_output_path, text_output_path, vocab_text_path
class CallEndAPIView(APIView):
    def post(self, request):
        audio_path, text_path, vocab_path = mergeRecordings()
        vocab_data = createVocabs(vocab_path)
        data = request.data.copy()
        data['converted_text_file'] = text_path
        data['recorded_audio_file'] = audio_path

        ai_user_id = request.data.get('ai_partner_id')

        try:
            ai_user_info = AI_User.objects.get(id=ai_user_id)
            data['language'] = ai_user_info.language.id
        except AI_User.DoesNotExist:
            return Response({'error': 'AI_User matching the provided ID does not exist.'},
                            status=status.HTTP_404_NOT_FOUND)

        current_date = date.today()
        formatted_date = current_date.strftime('%Y-%m-%d')
        data['date'] = formatted_date

        data['calling_time'] = get_audio_runtime(audio_path)

        os.remove(vocab_path)

        recording_serializer = RecordingSerializer(data=data)
        if recording_serializer.is_valid():
            recording_model = recording_serializer.save()
            vocab = {
                'user_id': recording_model.user_id,
                'recording_id': recording_model.id,
                'date' : formatted_date,
                'word_list': vocab_data
            }
            # print(vocab)
            vocab_serializer = VocabListSerializer(data=vocab)
            if vocab_serializer.is_valid():
                vocab_serializer.save()
                return Response(vocab_serializer.data, status=status.HTTP_201_CREATED)
            return Response(recording_serializer.data, status=status.HTTP_201_CREATED)
        return Response(recording_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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
