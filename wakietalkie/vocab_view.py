from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from wakietalkie.models import VocabList
from wakietalkie.serializers import VocabListSerializer

from django.shortcuts import get_object_or_404

# Helper function to serialize list of objects
def serialize_list(objects, serializer_class):
    serializer = serializer_class(objects, many=True)
    return serializer.data

# Helper function to serialize single object
def serialize_object(obj, serializer_class):
    serializer = serializer_class(obj)
    return serializer.data

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

class MostRecentVocabListView(APIView):
    def get(self, request, user_id):
        latest_vocab_list = VocabList.objects.filter(user_id=user_id).order_by('-id').first()
        if latest_vocab_list:
            serializer = VocabListSerializer(latest_vocab_list)
            return Response(serializer.data)
        else:
            return Response("no vocab list created yet!", status=status.HTTP_204_NO_CONTENT)
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
