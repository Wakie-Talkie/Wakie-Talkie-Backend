from django.db import models

# 언어
class Language(models.Model):
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
    profile_img = models.ImageField(upload_to='ai_user_profile_images/')
    description = models.TextField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

# 기록 모델
class Recording(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)  # User 모델을 ForeignKey로 참조
    ai_partner_id = models.ForeignKey(AI_User, on_delete=models.CASCADE)  # AI_User 모델을 ForeignKey로 참조
    date = models.DateField()
    calling_time = models.CharField(max_length=20)  # 문자열 형식으로 처리
    converted_text_file = models.TextField()
    recorded_audio_file = models.FileField(upload_to='recordings/')  # 파일 형식으로 처리

# 단어장
class VocabList(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)  # User 모델을 ForeignKey로 참조
    recording_id = models.ForeignKey(Recording, on_delete=models.CASCADE)  # Recording 모델을 ForeignKey로 참조
    word_list = models.JSONField()  # JSON 형식의 필드로 사용자 단어 리스트를 저장

    def __str__(self):
        return f"Vocab List {self.id} for User {self.user_id}"
