from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from wakietalkie.models import User
from wakietalkie.serializers import UserSerializer

from django.shortcuts import get_object_or_404

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
