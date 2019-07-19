from django.urls import path
from quiz import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login),
    path('signup/', views.signup),
    path('logout/', views.logout),
    path('question/', views.question_get),
    path('question/create/', views.QuestionCreateAPIView.as_view()),
    path('question/<int:question_id>/', views.CommentsCreateAPIView.as_view())
]
