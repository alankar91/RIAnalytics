from django.urls import path, include
from .views import *

urlpatterns = [
  path('mainpage', social_page, name='social_mainpage'),
  path('socialform', social_form_processing, name='social_form'),
  path('generate', social_generate, name='social_generate'),
  
]