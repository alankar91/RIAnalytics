from django.urls import path, include
from .views import *

urlpatterns = [
  path('mainpage', text_page, name='text_mainpage'),
  path('textform', text_form_processing, name='text_form'),
  path('generate', text_generate, name='text_generate'),
]