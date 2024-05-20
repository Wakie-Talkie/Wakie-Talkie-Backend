from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from .serializers import *

from wakietalkie.models import AI_User
from wakietalkie.serializers import AIUserSerializer

from django.shortcuts import get_object_or_404

# Helper function to serialize list of objects
def serialize_list(objects, serializer_class):
    serializer = serializer_class(objects, many=True)
    return serializer.data

# Helper function to serialize single object
def serialize_object(obj, serializer_class):
    serializer = serializer_class(obj)
    return serializer.data


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
