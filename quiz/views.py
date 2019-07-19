from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from quiz import serializers
from pytesseract import image_to_string
from PIL import Image
import os
from quiz import models
from django.contrib.auth import login, authenticate, logout
from rest_framework.generics import CreateAPIView, RetrieveAPIView
import json

def detect_text(image):
    image = Image.open(image)
    return image_to_string(image)


@api_view(['GET', 'POST'])
def index(request):
    if request.method == 'GET':
        return Response(status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = serializers.ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            path = os.getcwd() + serializer.data['image']
            texts = detect_text(path)
            data = {"texts": texts}
            return Response(data, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        print(username, password)
        user = authenticate(username=username, password=password)
        print(user)
        if user:
            data = {'token':user.auth_token.key}
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def signup(request):
    print(request.data)
    serializer = serializers.UserSignUpSerializer(data=request.data)
    if serializer.is_valid():
        print(serializer.validated_data)
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionCreateAPIView(CreateAPIView):
    serializer_class = serializers.QuestionCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['GET'])
def question_get(request):
    if request.method == 'GET':
        questions = models.Question.objects.all()[:10]
        data = serializers.QuestionListSerializer(questions, many=True)
        return Response(data.data, status=status.HTTP_200_OK)


class CommentsCreateAPIView(CreateAPIView):
    serializer_class = serializers.CommentCreateSerializer

    def perform_create(self, serializer):
        question = models.Question.objects.get(id=self.kwargs.get('question_id'))
        data = serializer.save(user=self.request.user)
        print(data)
        question.comments.add(data)


