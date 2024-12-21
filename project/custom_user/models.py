from django.db import models
from django_use_email_as_username.models import BaseUser, BaseUserManager
from django.contrib.postgres.fields import JSONField


class User(BaseUser):
    email = models.EmailField(max_length=100, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = BaseUserManager()

    def __str__(self):
        return self.email



class Question(models.Model):
    question=models.CharField(max_length=200)
    right=models.CharField(max_length=200)


class History(models.Model):
    history_id=models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    summary = models.TextField()
    model_name=models.CharField(max_length=200)
    right_selected=models.TextField()




    def __str__(self):
        return f"Session for {self.user.username} at {self.date}"
