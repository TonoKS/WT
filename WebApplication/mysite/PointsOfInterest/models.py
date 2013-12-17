from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.core import validators
from datetime import datetime 


class Friend(models.Model):
	who = models.ForeignKey(User, related_name='who')
	fwith = models.ForeignKey(User, related_name='withwho')
	dateCreated = models.DateTimeField(default=datetime.now)
	confirmed = models.BooleanField(default=False)


class PointOfInterest(models.Model):
	userid = models.ForeignKey(User)
	latitude = models.FloatField(max_length=30)
	longitude = models.FloatField(max_length=30)
	title = models.CharField(max_length=30)
	description = models.CharField(max_length=200)
	dateCreated =  models.DateTimeField()
	dateModified =  models.DateTimeField(null=True, blank=True)
	category = models.CharField(max_length=1)
	
class Commentary(models.Model):
	userid = models.ForeignKey(User)
	poiid = models.ForeignKey(PointOfInterest)
	commentary = models.CharField(max_length=300)
	dateCreated =  models.DateTimeField()

"""
p- private
f- fiends
o- opened
"""

CATEGORIES = (('p', 'Súkromne'),
							('f', 'Pre priateľov'),
							('o', 'Verejné'))
							

class CreatePoiForm(forms.Form):
	title = forms.CharField(widget=forms.TextInput(attrs={'size' : 25}), required=True, max_length=30, initial="")
	description = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows' : 5, 'cols' : 40, 'resize' : "none"}), max_length=200, initial="")
	latitude = forms.CharField(widget=forms.HiddenInput, initial="")
	longitude = forms.CharField(widget=forms.HiddenInput, initial="")
	category = forms.ChoiceField(required=True, widget=forms.RadioSelect, choices=CATEGORIES)

class LoginForm(forms.Form):
	username = forms.CharField(required=True, max_length=30, initial="")
	password = forms.CharField(max_length=32, required=True, widget=forms.PasswordInput, initial="")
	def clean(self):
		cleaned_data = self.cleaned_data # individual field's clean methods have already been called
		username = cleaned_data.get('username')
		password = cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		if user is None:
			raise forms.ValidationError("Neplatný login alebo heslo.")
		return cleaned_data
	#widget=forms.HiddenInput

class RegistrationForm(forms.Form):
	username = forms.CharField(validators=[RegexValidator(regex=r'[a-zA-Z0-9]{3,}', message='Login musí byť dlhý minimálne 3 znaky, povolené sú písmena a číslice', code='error')], required=True, max_length=30, initial="")
	email = forms.EmailField(required=True, max_length=50, initial="")
	password = forms.CharField(validators=[RegexValidator(regex=r'[a-zA-Z0-9]{6,}', message='Heslo musí byť hlhé minimálne 6 znakov, povolené sú písmena a číslice', code='error')], max_length=32, required=True, widget=forms.PasswordInput, initial="")
	passagain = forms.CharField(max_length=32, required=True, widget=forms.PasswordInput, initial="")
	def clean(self):
		cleaned_data = self.cleaned_data # individual field's clean methods have already been called
		password1 = cleaned_data.get("password")
		password2 = cleaned_data.get("passagain")
		if password1 != password2:
			raise forms.ValidationError("Heslá musia byť identické.")
		username1 = cleaned_data.get("username")
		exist = User.objects.filter(username = username1).first()
		if exist is not None:
			raise forms.ValidationError("Tento login je už obsadený.")
		return cleaned_data

	
class CommentaryForm(forms.Form):
	commentary = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows' : 4,  'resize' : "none"}), max_length=300, initial="")
	
class FindForm(forms.Form):
	username = username = forms.CharField(validators=[RegexValidator(regex=r'[a-zA-Z0-9]{3,}', message='Vyhľadávaný reťazec musí byť dlhý minimálne 3 znaky, povolené sú písmena a číslice', code='error')],required=True, max_length=30, initial="");


# Create your models here.
