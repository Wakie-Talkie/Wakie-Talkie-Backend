import os

from django.http import FileResponse, Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from wakietalkie.models import Recording
from wakietalkie.serializers import RecordingSerializer

from django.shortcuts import get_object_or_404

# Helper function to serialize list of objects
def serialize_list(objects, serializer_class):
    serializer = serializer_class(objects, many=True)
    return serializer.data

# Helper function to serialize single object
def serialize_object(obj, serializer_class):
    serializer = serializer_class(obj)
    return serializer.data

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

class RecordingGetRecordAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Recording, pk=pk)

    def get(self, request, pk):
        recording = self.get_object(pk)
        file_path = recording.recorded_audio_file
        # Check if the file exists
        if not os.path.exists(file_path):
            raise Http404("File not found")

        # Serve the file
        response = FileResponse(open(file_path, 'rb'), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filepath="combined_recording.mp3"'
        return response
class RecordingGetTextAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Recording, pk=pk)

    def get(self, request, pk):
        recording = self.get_object(pk)
        file_path = recording.converted_text_file
        # Check if the file exists
        if not os.path.exists(file_path):
            raise Http404("File not found")

        # Serve the file
        response = FileResponse(open(file_path, 'rb'), content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filepath="combined_recording.txt"'
        return response

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