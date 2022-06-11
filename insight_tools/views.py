from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from .forms import *
from RIAnalytics.settings import FILES_DIR
import os
from .wordAnalytics import  WordAnalyst
# Create your views here.
info = {
  'reportFilename':'',
  'keywordFilename':'',
  'keywords':None,
}
def insights_page(request):
  return render(request, 'insights.html')

def insights_generate(request):
  analyst = WordAnalyst(info['reportFilename'], info['keywordFilename'])
  try:
    report = analyst.generateHTML()
    return JsonResponse({'status':'successful', 'report':report})
  except Exception as E:
    print('Error',str(E))
    return JsonResponse({'status':'Failed', 'report':''})


def handle_uploaded_file(f, filename):
    with open(os.path.join(FILES_DIR,filename), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def insights_form_processing(request):
    if request.method == 'POST':
      insights_form = insightsAnalyticsForm(request.POST)
      all_files = []
      my_files=request.FILES.getlist('report_files')
      if insights_form.is_valid():
          for f in my_files:
              all_files.append(f.name)    
              handle_uploaded_file(f, f.name)
          keyfile = request.FILES['keyword_file']
          info['keywordFilename'] = keyfile.name
          handle_uploaded_file(keyfile, keyfile.name)
          info['reportFilename'] = all_files
          if request.is_secure():
            protocol = 'https'
          else:
            protocol = 'http'

          domain = protocol + "://" + request.META['HTTP_HOST']

          return render(request,'text_report.html', context={'mode':'Insights','files':'', 'url': f'{domain}/insights/generate','statusurl': f'{domain}/returnIstatus'})
      else:
          return render(request,'insights.html', context={'insightsform':insights_form})

      
    return HttpResponseRedirect(reverse('insights_mainpage'))