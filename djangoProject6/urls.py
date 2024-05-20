"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


# djangoProject6/urls.py

from django.contrib import admin
from django.urls import path, include
from wakietalkie import views
from django.views.generic.base import RedirectView
from django.urls import path

from wakietalkie.ai_view import *
from wakietalkie.user_view import *
from wakietalkie.vocab_view import *
from wakietalkie.language_view import *
from wakietalkie.recording_view import *
from wakietalkie.views import *

from django.contrib import admin
from django.urls import path, include
from wakietalkie.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    # User API endpoints
    path('users/', UserListCreateAPIView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),
    path('users/create/', UserListCreateAPIView.as_view(), name='user-create'),
    path('users/update/<int:pk>/', UserDetailAPIView.as_view(), name='user-update'),
    path('users/delete/<int:pk>/', UserDetailAPIView.as_view(), name='user-delete'),
    path('users/<int:user_id>/update/profile_img/', UserDetailAPIView.as_view(), name='user-update-profile-img'),
    path('users/<int:user_id>/update/nickname/', UserDetailAPIView.as_view(), name='user-update-nickname'),
    path('users/<int:user_id>/update/want_language/', UserDetailAPIView.as_view(), name='user-update-want-language'),
    path('users/<int:user_id>/update/description/', UserDetailAPIView.as_view(), name='user-update-description'),

    #language API
    path('languages/', LanguageListCreateAPIView.as_view(), name='language-list'),

    # AI User API endpoints
    path('ai-users/', AIUserListCreateAPIView.as_view(), name='ai-user-list'),
    path('ai-users/<int:pk>/', AIUserDetailAPIView.as_view(), name='ai-user-detail'),
    path('ai-users/create/', AIUserListCreateAPIView.as_view(), name='ai-user-create'),
    path('ai-users/update/<int:pk>/', AIUserDetailAPIView.as_view(), name='ai-user-update'),
    path('ai-users/delete/<int:pk>/', AIUserDetailAPIView.as_view(), name='ai-user-delete'),
    path('ai-users/language/<int:language_id>/', AIUserListByLanguageAPIView.as_view(), name='ai-user-list-by-language'),
    # Recording API endpoints
    path('recordings/', RecordingListCreateAPIView.as_view(), name='recording-list'),
    path('recordings/<int:pk>/', RecordingDetailAPIView.as_view(), name='recording-detail'),
    path('recordings/create/', RecordingListCreateAPIView.as_view(), name='recording-create'),
    path('recordings/update/<int:pk>/', RecordingDetailAPIView.as_view(), name='recording-update'),
    path('recordings/delete/<int:pk>/', RecordingDetailAPIView.as_view(), name='recording-delete'),
    path('recordings/user/<int:user_id>/', RecordingListByUserView.as_view(), name='recording-list-by-user'),

    # VocabList API endpoints
    path('vocab-lists/', VocabListListCreateAPIView.as_view(), name='vocab-list-list'),
    path('vocab-lists/<int:pk>/', VocabListDetailAPIView.as_view(), name='vocab-list-detail'),
    path('vocab-lists/create/', VocabListListCreateAPIView.as_view(), name='vocab-list-create'),
    path('vocab-lists/update/<int:pk>/', VocabListDetailAPIView.as_view(), name='vocab-list-update'),
    path('vocab-lists/delete/<int:pk>/', VocabListDetailAPIView.as_view(), name='vocab-list-delete'),
    path('vocab-lists/latest/', LatestVocabListView.as_view(), name='latest-vocab-list'),
    path('vocab-lists/', VocabListView.as_view(), name='vocab-list'),

    #STT,GPT,TTS에 관한 엔드포인트
    path('upload-audio/', AudioFileUploadNoDB.as_view(), name='audio_upload'),
    path('stt/transcription/', TranscriptionRetrieve.as_view(), name='stt_transcription'),
    path('result/', SttGptTtsResponse.as_view(), name='stt_gpt_tts_response'),
    # TTS로 생성된 음성 데이터를 반환하는 엔드포인트
    path('tts-audio/', TtsResponse.as_view(), name='tts_audio_response'),

    # 전체 대화 스크립트를 반환하는 엔드포인트
    path('conversation/', ConversationScriptAPIView.as_view(), name='conversation_script'),
    #call 관련 엔드포인트 시작,끝,끝난 후 정보
    path('call/start/', CallStartAPIView.as_view(), name='call-start'),
    path('call/end/', CallEndAPIView.as_view(), name='call-end'),
    path('call/info/', CallInfoAPIView.as_view(), name='call-info'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



