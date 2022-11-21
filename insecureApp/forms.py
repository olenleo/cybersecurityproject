from django import forms
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from .models import InsecureUser

class NewUserForm(UserCreationForm):

	class Meta:
		model = InsecureUser
		fields = ("USERNAME_FIELD", "securityAnswer", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		if commit:
			user.save()
		return user