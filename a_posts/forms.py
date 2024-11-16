from django import forms
from .models import Post, Comment, Reply

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['url','body','tag']
        labels = {
            'body':'Caption',
            'tag':'Category'
        }
        widgets = {
            'body': forms.Textarea(attrs={'rows':3, 'placeholder':'Add a caption...', 'class' : 'font1 text-4xl'}),
            'url': forms.TextInput(attrs={'placeholder':'Add URL...'}),
            'tag':forms.CheckboxSelectMultiple(),
        }
        
class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['body', 'tag']
        labels = {
            'body':'',
            'tag':'Category'
        }
        widgets = {
            'body': forms.Textarea(attrs={'rows':3, 'class' : 'font1 text-4xl'}),
            'tag':forms.CheckboxSelectMultiple(),
        }
        
class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        labels = {
            'body':'',
        }
        widgets = {
            'body': forms.TextInput(attrs={'placeholder':'Add a comment....'}),
            
        }
        
class ReplyCreateForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['body']
        labels = {
            'body':'',
        }
        widgets = {
            'body': forms.TextInput(attrs={'placeholder':'Add Reply....', 'class':'!text-sm'}),
            
        }