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