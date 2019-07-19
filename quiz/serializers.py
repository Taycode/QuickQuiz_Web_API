from rest_framework import serializers
from quiz import models
from django.contrib.auth.models import User


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = '__all__'


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class QuestionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = '__all__'


class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = ['user', 'question']


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ['user', 'comment']
