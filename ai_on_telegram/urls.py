from django.contrib import admin
from django.urls import path

from bot.views import telegram_webhook

urlpatterns = [
    path('webhook', telegram_webhook, name="telegram-webhook"),
    path('admin/', admin.site.urls),
]
