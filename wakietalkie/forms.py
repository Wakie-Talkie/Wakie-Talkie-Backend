from django import forms
from .models import User, AI_User, Alarm

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname', 'profile_img', 'description', 'language', 'want_language']
class AI_UserForm(forms.ModelForm):
    class Meta:
        model = AI_User
        fields = ['nickname', 'profile_img', 'description', 'language']

class AlarmForm(forms.ModelForm):
    class Meta:
        model = Alarm
        fields = ['User_id', 'partner_id', 'date', 'received_time', 'converted_textfile', 'recorded_audiofile', 'converted_textfile_piece', 'recorded_audiofile_piece']