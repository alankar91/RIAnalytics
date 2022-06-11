from django.db import models

# Create your models here.
class socialAnalyticsModel(models.Model):
    
    handles_files = models.FileField(upload_to='files/', blank=True, null=True)              
    keyword_file = models.FileField(upload_to='files/', blank=True, null=False)
    keywords = models.CharField(max_length=500, blank=True, null=True)
    no_of_tweets = models.IntegerField(blank=True, null=False)
    consumer_key= models.CharField(max_length=500, blank=True, null=True)
    access_token = models.CharField(max_length=500, blank=True, null=True)
    consumer_secret= models.CharField(max_length=500, blank=True, null=True)
    access_token_secret =  models.CharField(max_length=500, blank=True, null=True)
