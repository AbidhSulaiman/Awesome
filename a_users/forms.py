from django import forms
from .models import Profile



# class ProfileForm(forms.ModelForm):  
#     class Meta:
#         model = Profile
#         fields = '__all__'
        
        
class ProfileForm(forms.ModelForm):  
    class Meta:
        model = Profile
        exclude = ['user']
        labels = {
            'real_name':'Name'
        }
        widgets = {
            'image':forms.FileInput(),
            'bio':forms.Textarea(attrs={'rows':3})
        }