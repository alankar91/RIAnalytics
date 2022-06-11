from django import forms
from .models import socialAnalyticsModel 

class socialAnalyticsForm(forms.ModelForm):
    class Meta:
        model = socialAnalyticsModel
        fields = '__all__'