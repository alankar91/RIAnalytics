from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .forms import textAnalyticsForm
from RIcore.functions import handle_uploaded_file
from RIAnalytics.settings import FILES_DIR
import os
from .txtInsight import TextAnalyst 
# Create your views here.
info = {
  'reportFilename':'', 
  'keywordFilename':'',
  'keywords':'',
  'report':'',
  }

def text_page(request):
  text_form = textAnalyticsForm()
  return render(request,'text_insights.html', context={'textform':text_form})

def text_generate(request):
  analyst = TextAnalyst()
  try:
    report = analyst.generateHTML(info['reportFilename'], info['keywordFilename'],info['keywords'])
    return JsonResponse({'status':'successful', 'report':report})
  except Exception as E:
    print('Error', str(E))
    return JsonResponse({'status':'Failed', 'report':''})

def handle_uploaded_file(f, filename):
    with open(os.path.join(FILES_DIR,filename), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def text_form_processing(request):
    if request.method == 'POST':
      text_form = textAnalyticsForm(request.POST)
      all_files = []
      my_files= request.FILES.getlist('report_files')
      if text_form.is_valid():
        print('valid form')
        for f in my_files:
          info['reportFilename'] = f.name
          all_files.append(f.name)
          handle_uploaded_file(f, f.name)
        keyfile = request.FILES['keyword_file']
        info['keywordFilename'] = keyfile.name
        handle_uploaded_file(keyfile, keyfile.name)
        info['keywords'] = text_form.cleaned_data['keywords'],

        if request.is_secure():
          protocol = 'https'
        else:
          protocol = 'http'

        domain = protocol + "://" + request.META['HTTP_HOST']

        return render(request,'text_report.html', context={'mode':'Text','files':all_files, 'url': f'{domain}/text/generate','statusurl': f'{domain}/returnstatus'})
      # if text_form.is_valid():
        
      #   '''
      #   load mode tells the page that it needs to generate the insights
      #   '''
      #   info['reportFilename'] = request.FILES['report_file'].name, 
      #   info['keywordFilename'] = request.FILES['keyword_file'].name,
    
      else:
        print('invalid Form')
        print(text_form.errors)
        return render(request,'text_insights.html', context={'textform':text_form})
    return HttpResponseRedirect(reverse('text_mainpage'))