"""RIAnalytics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .settings import STATIC_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('RIcore.urls')),
    path('insights/', include('insight_tools.urls')),
    path('news/', include('news_analytics.urls')),
    path('social/', include('social_analytics.urls')),
    path('text/', include('text_analytics.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


