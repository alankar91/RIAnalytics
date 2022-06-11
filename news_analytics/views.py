from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .forms import *
from RIAnalytics.settings import FILES_DIR
import os
from .newsInsight import NewsAnalyst
# Create your views here.

info = {
  'reportFilename':'',
  'keywordFilename':'',
  'keywords':None,
}


def news_page(request):
  return render(request,'news_insights.html')


def handle_uploaded_file(f, filename):
    with open(os.path.join(FILES_DIR,filename), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def news_generate(request):
	analyst = NewsAnalyst()
	print('gotten analyst')
	try:
		print('generating reposer')
		report = analyst.generateHTML(info['reportFilename'], info['keywordFilename'])
		print('report done')
		return JsonResponse({'status':'successful', 'report':report})
	except Exception as E:
		print('Error',str(E))
		return JsonResponse({'status':'Failed', 'report':''})
		
# def get_news(request):
# 	if request.is_secure():
# 		protocol = 'https'
# 	else:
# 		protocol = 'http'

# 	domain = protocol + "://" + request.META['HTTP_HOST']

# 	return render(request,'text_report.html', context={'mode':'News','files':[], 'url': f'{domain}/news/generate','statusurl': f'{domain}/returnNstatus'})

def news_form_processing(request):
    if request.method == 'POST':
      news_form = newsAnalyticsForm(request.POST)
      my_files = request.FILES.getlist('input_files')
      all_files = []
      if news_form.is_valid():
          for f in my_files:
              all_files.append(f.name)
              info['reportFilename'] = f.name
              handle_uploaded_file(f, f.name)

          keyfile = request.FILES['keyword_file']
          info['keywordFilename'] = keyfile.name
          handle_uploaded_file(keyfile, keyfile.name)            

          if request.is_secure():
            protocol = 'https'
          else:
            protocol = 'http'

          domain = protocol + "://" + request.META['HTTP_HOST']

          return render(request,'text_report.html', context={'mode':'News','files':all_files, 'url': f'{domain}/news/generate','statusurl': f'{domain}/returnNstatus'})
      else:
          print(news_form.errors)
          return render(request,'news_insights.html', context={'newsform':news_form})
      

    return HttpResponseRedirect(reverse('news_mainpage'))