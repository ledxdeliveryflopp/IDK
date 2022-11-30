from datetime import timezone, datetime, date, timedelta
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
    username = models.CharField(max_length=30, unique=True, null=False, help_text='Логин',
                                error_messages={'unique': "Такой пользователь уже существует!"})
    avatar = models.ImageField(upload_to='images/avatars/', verbose_name='Аватарка')

    def __str__(self):
        return self.username


class Question(models.Model):
    question_text = models.CharField(max_length=200, verbose_name='Название')
    pub_date = models.DateTimeField(default=datetime.today(), null=False, verbose_name='Дата')
    life_time = models.DateTimeField(default=datetime.today() + timedelta(days=1),
                                     verbose_name='Время жизни',
                                     null=False)
    full_info = models.CharField(max_length=50, null=False, verbose_name='полное описание')
    short_info = models.CharField(max_length=25, null=False, verbose_name='краткое описание')
    question_image = models.ImageField(upload_to='images/questions/', verbose_name='картинка')
    votes = models.IntegerField(default=0, verbose_name='коллво голосов')
    voted_by = models.ManyToManyField(CustomUser, verbose_name='проголосовавшие', blank=True)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def persentc(self):
        return round(100 * self.votes / self.question.votes)

    def __str__(self):
        return self.choice_text
