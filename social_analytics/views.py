from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from .forms import *
from RIAnalytics.settings import FILES_DIR
import os
from .socialAnalytics import SocialAnalyst
info = {}
# Create your views here.
def social_page(request):
  return render(request,'social_media.html')

def handle_uploaded_file(f, filename):

    with open(os.path.join(FILES_DIR,filename), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def social_generate(request):
  analyst = SocialAnalyst()
  try:
    report = analyst.generateHTML(info['authKeys'], info['Twitter_Handles_File'],info['tweet_count'])
    report('Successfull')
    return JsonResponse({'status':'successful', 'report':report})
  except Exception as E:
    print('Error', str(E))
    return JsonResponse({'status':'Failed', 'report':''})

def social_form_processing(request):
    if request.method == 'POST':
      social_form = socialAnalyticsForm(request.POST, request.FILES)
      
      if social_form.is_valid():
        files = request.FILES
        authKeys = []
        sform = social_form.cleaned_data
        authKeys[sform['consumer_key'], sform['consumer_key'], sform['access_token'], sform['access_token_secret']]
        tweet_count = sform['no_of_tweets']
        twit_handles = sform['keywords']
        if 'handles_files' in files.keys():
          twit_handles = files['handles_files'].name

        info['authKeys'] = authKeys
        info['Twitter_Handles_File'] = twit_handles
        info['tweet_count'] = tweet_count

        for item in files.items():
          f = item[1]
          handle_uploaded_file(f, f.name)

        if request.is_secure():
          protocol = 'https'
        else:
          protocol = 'http'

        domain = protocol + "://" + request.META['HTTP_HOST']

        return render(request,'text_report.html', context={'mode':'Social','files':'', 'url': f'{domain}/social/generate','statusurl': f'{domain}/returnSstatus'})
          
      else:
        print(social_form.errors)
    return HttpResponseRedirect(reverse('social_mainpage'))