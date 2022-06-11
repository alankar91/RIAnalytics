from django import forms
from .models import newsAnalyticsModel 

class newsAnalyticsForm(forms.ModelForm):
    class Meta:
        model = newsAnalyticsModel
        fields = '__all__'