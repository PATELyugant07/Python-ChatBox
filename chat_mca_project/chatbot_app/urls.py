# chatbot_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_home, name='chat_home'),
    path('chat/', views.chat_response, name='chat_response'),
    path('summarize/', views.summarize_chat, name='summarize_chat'),
]