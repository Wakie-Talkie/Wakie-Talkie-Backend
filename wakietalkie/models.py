from django.db import models

# 사용자 정보 모델
class User(models.Model):
    ID = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=20)
    profile_img = models.ImageField(upload_to='user_profile_images/')
    description = models.TextField()
    language = models.ForeignKey('Language', on_delete=models.CASCADE)
    want_language = models.CharField(max_length=20)

    def __str__(self):
        return self.nickname

# AI 사용자 정보 모델
class AI_User(models.Model):
    ID = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=20)
    profile_img = models.ImageField(upload_to='ai_user_profile_images/')
    description = models.TextField()
    language = models.ForeignKey('Language', on_delete=models.CASCADE)

    def __str__(self):
        return self.nickname

# 알람 정보 모델
class Alarm(models.Model):
    ID = models.AutoField(primary_key=True)
    User_id = models.IntegerField()
    partner_id = models.IntegerField()
    date = models.DateField()
    received_time = models.DateTimeField()
    converted_textfile = models.TextField()
    recorded_audiofile = models.TextField()
    converted_textfile_piece = models.TextField()
    recorded_audiofile_piece = models.TextField()

# 언어 정보 모델
class Language(models.Model):
    code = models.CharField(max_length=2, unique=True, default='ko')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    @classmethod
    def add_initial_languages(cls):
        cls.objects.bulk_create([
            cls(code='ko', name='한국어'),
            cls(code='en', name='영어'),
            cls(code='ja', name='일본어'),
            # 다른 언어를 추가할 수 있습니다.
        ])

