from django import forms
import logging
logger = logging.getLogger(__name__)

from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from .models import  Message

class NewUserForm(UserCreationForm):

	class Meta:
		fields = ("USERNAME_FIELD", "securityAnswer", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		if commit:
			user.save()
		return user

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ("message_text",)
    
    def save(self, commit=True):
        message = super(MessageForm, self).save(commit=False)
        
        if commit:
            print('mESSAGEs')
            message.save()
        return message
