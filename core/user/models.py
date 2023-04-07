from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class BaseModel(models.Model):
    create_at = models.DateTimeField(auto_now=True)
    update_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True


class User(AbstractUser):
    
    def __str__(self) -> str:
        return self.username

class UserBlog(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    blog = models.TextField(max_length=2500)
    