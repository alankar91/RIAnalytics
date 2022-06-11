from django.urls import path, include
from .views import *

urlpatterns = [
  path('mainpage', insights_page, name='insights_mainpage'),
  path('generate', insights_generate, name='insights_generate'),
  path('insightsform', insights_form_processing, name='insights_form')
]