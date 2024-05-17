from django import forms
from .models import User, AI_User, Recording, VocabList, Language

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname', 'profile_img', 'description', 'language', 'want_language']

class AI_UserForm(forms.ModelForm):
    class Meta:
        model = AI_User
        fields = ['nickname', 'profile_img', 'description', 'language']
class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['name']


class RecordingForm(forms.ModelForm):
    class Meta:
        model = Recording
        fields = ['user_id', 'ai_partner_id', 'date', 'calling_time', 'converted_text_file', 'recorded_audio_file', 'language']

class VocabListForm(forms.ModelForm):
    class Meta:
        model = VocabList
        fields = ['user_id', 'recording_id', 'word_list']
