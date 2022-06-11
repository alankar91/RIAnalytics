from django.urls import path, include
from .views import *

urlpatterns = [
  path('',index_page),
  path('about',about_page),
  path('contact',contact_page),
  path('services',services_page),
  path('returnstatus',return_status),
  path('returnNstatus',return_status_news),
  path('returnSstatus',return_status_socials),
  path('returnIstatus',return_status_insights),
  path('download/<str:file>',download_highlights),
]