from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import *

# Helper function to serialize list of objects
def serialize_list(objects, serializer_class):
    serializer = serializer_class(objects, many=True)
    return serializer.data

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