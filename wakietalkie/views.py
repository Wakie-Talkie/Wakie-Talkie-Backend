from django.shortcuts import render, get_object_or_404, redirect
from .models import User, AI_User, Language
from .forms import UserForm, AI_UserForm, RecordingForm, VocabListForm
from rest_framework import generics
from .models import User, AI_User
from .serializers import UserSerializer, AIUserSerializer
from openai import OpenAI
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from .models import User, AI_User, Recording, VocabList
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from . import serializers
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
        language_id = self.request.query_params.get('language', None)
        if language_id is not None:
            return AI_User.objects.filter(language=language_id)
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
