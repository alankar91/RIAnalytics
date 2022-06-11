from django import forms
from .models import textAnalyticsModel 

class textAnalyticsForm(forms.ModelForm):
    class Meta:
        model = textAnalyticsModel
        fields = '__all__'
        widgets={"report_files":forms.FileInput(attrs={'id':'report_files','required':True,'multiple':True})}