from rangedogs.rangereport.models import *
from django.forms import ModelForm

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile

class GunForm(ModelForm):
    class Meta:
        model = Gun
