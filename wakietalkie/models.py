from django.db import models
from django.utils import timezone

# 언어
class Language(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# 사용자 정보 모델
class User(models.Model):
    id = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=100)
    profile_img = models.ImageField(upload_to='user_profile_images/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    want_language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='wanted_by')

# AI 사용자 정보 모델
class AI_User(models.Model):
    id = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=100)
    profile_img = models.ImageField(upload_to='ai_user_profile_images/', null=True, blank=True)
    ai_type = models.CharField(max_length=100)
    description = models.TextField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

# 기록 모델
class Recording(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    ai_partner_id = models.IntegerField()
    date = models.CharField(max_length=20)
    calling_time = models.CharField(max_length=20)
    converted_text_file = models.CharField(max_length=100)
    recorded_audio_file = models.CharField(max_length=100)
    #caller = models.ForeignKey(User, related_name='call_records', on_delete=models.CASCADE)  # 전화를 건 사용자 정보
    language = models.IntegerField()

    def __str__(self):
        return f"Recording {self.id}"

# 단어장
class VocabList(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    recording_id = models.IntegerField()
    date = models.CharField(max_length=20)
    word_list = models.JSONField()  # JSON 형식의 필드로 사용자 단어 리스트를 저장

    def __str__(self):
        return f"Vocab List {self.id} for User {self.user_id}"

# 전화 기록 모델
class CallRecord(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)  # 전화 시작 시간을 저장하는 필드. 자동으로 생성됨.
    end_time = models.DateTimeField(null=True, blank=True)  # 전화 종료 시간을 저장하는 필드. 비어있을 수 있음.
    ai_user = models.ForeignKey(AI_User, on_delete=models.CASCADE)  # 전화를 한 AI 사용자를 나타내는 필드

    def __str__(self):
        return f"Call Record for AI User {self.ai_user.nickname}"  # 전화 기록 모델의 문자열 표현
