# ChatMCA/urls.py

from django.contrib import admin
from django.urls import path, include
from chatbot_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # This is the line you need to fix the 404 error
    path('api/', include('chatbot_app.urls')),
    path('', views.chat_home, name='chat_home'), # This is for your main page
]