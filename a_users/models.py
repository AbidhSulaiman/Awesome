from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avathars/', null=True, blank=True)
    real_name = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    location = models.CharField(max_length=20, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    
    
    def __str__(self):
        return str(self.user)
    
    @property
    def avathar(self):
        try:
            avathar = self.image.url
            
        except:
            avathar = static('images/avatar_default.svg')
            
        return avathar
    
    @property
    def name(self):
        if self.real_name:
            name = self.real_name
        else:
            name = self.user.username
        return name

