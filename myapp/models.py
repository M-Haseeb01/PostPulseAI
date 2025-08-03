from django.db import models

# Create your models here.
from django.db import models

class User(models.Model):
    name=models.CharField(max_length=128)
    age=models.IntegerField()
    email=models.EmailField( max_length=254,unique=True)
    password=models.CharField(max_length=128)
    def __str__(self):
        return self.name
    
    
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=128)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__ (self):
        return self.title
    
    