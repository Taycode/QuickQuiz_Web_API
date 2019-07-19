from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token


class Image(models.Model):
    image = models.FileField(upload_to='photo')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True)
    comment = models.CharField(max_length=100)
    upvote = models.IntegerField(default=0)
    downvote = models.IntegerField(default=0)


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True)
    question = models.CharField(max_length=100)
    comments = models.ManyToManyField(Comment)


def create_token(sender, **kwargs):
    if kwargs['created']:
        Token.objects.create(user=kwargs['instance'])


post_save.connect(create_token, sender=User)
