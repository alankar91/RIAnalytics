from django.db import models

# Create your models here.
class textAnalyticsModel(models.Model):
                  
    report_files = models.FileField(upload_to='files/', blank=True, null=False)
    keyword_file = models.FileField(upload_to='files/', blank=True, null=False)
    keywords = models.CharField(max_length=500, blank=True, null=True)