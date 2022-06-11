from django.db import models

# Create your models here.
class insightsAnalyticsModel(models.Model):
                  
    report_files = models.FileField(upload_to='files/', blank=True, null=False)
    keyword_file = models.FileField(upload_to='files/', blank=True, null=False)