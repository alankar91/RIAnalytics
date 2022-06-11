from django.urls import path, include
from .views import *

urlpatterns = [
  path('mainpage', news_page, name='news_mainpage'),
  path('newsform', news_form_processing, name='news_form'),
  path('generate', news_generate, name='news_generate'),
  # path('fakegen', get_news, name='fakenews_generate'),
]