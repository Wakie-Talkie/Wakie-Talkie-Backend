from rest_framework import serializers
from .models import User, AI_User, Recording, VocabList, Language

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class AIUserSerializer(serializers.ModelSerializer):
    profile_img_url = serializers.SerializerMethodField()
    class Meta:
        model = AI_User
        fields = '__all__'
    def get_profile_img_url(self, obj):
        request = self.context.get('request')
        if obj.profile_img:
            return request.build_absolute_uri(obj.profile_img.url)
        return None
class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

class RecordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recording
        fields = '__all__'

class VocabListSerializer(serializers.ModelSerializer):
    class Meta:
        model = VocabList
        fields = '__all__'


class AudioFileSerializer(serializers.ModelSerializer):
    # ai_user_id = serializers.IntegerField()

    class Meta:
        model = Recording
        fields = ['recorded_audio_file', 'ai_partner_id', 'user_id','language']  # 오디오 파일만을 필드로 포함시킵니다.
