from django.shortcuts import render
import os
from django.http import JsonResponse, Http404, HttpResponse
from RIAnalytics.settings import OUTPUT_DIR
# Create your views here.

info = {'stat':1, 'doing':True}
## stat represents the current status
## doing is a key used to terminate or initate the while loop
def index_page(request):
  return render(request,'index.html')
  
def about_page(request):
  return render(request,'about-us.html')
  
def services_page(request):
  return render(request,'our-services.html')
  
def contact_page(request):
  return render(request,'contact-us.html')  

def download_highlights(request, file):
  file_path = os.path.join(OUTPUT_DIR, file)

  if os.path.exists(file_path):
      with open(file_path, 'rb') as fh:
          response = HttpResponse(fh.read(), content_type="application/pdf")
          response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
          return response
  raise Http404
  

def return_status(request):
  from text_analytics.txtInsight import info as inf
  if inf['STATUS'] == 'QUIT' :
    return JsonResponse({'value':'end'})
  else:
    return JsonResponse({'value':inf['STATUS']})

def return_status_news(request):
  from news_analytics.newsInsight import info as inf
  if inf['STATUS'] == 'QUIT' :
    print(inf['STATUS'])
    return JsonResponse({'value':'end'})
  else:
    print(inf['STATUS'])
    return JsonResponse({'value':inf['STATUS']})

def return_status_socials(request):
  from social_analytics.socialAnalytics import info as inf
  if inf['STATUS'] == 'QUIT' :
    print(inf['STATUS'])
    return JsonResponse({'value':'end'})
  else:
    print(inf['STATUS'])
    return JsonResponse({'value':inf['STATUS']})


def return_status_insights(request):
  from insight_tools.wordAnalytics import info as inf
  if inf['STATUS'] == 'QUIT' :
    print(inf['STATUS'])
    return JsonResponse({'value':'end'})
  else:
    print(inf['STATUS'])
    return JsonResponse({'value':inf['STATUS']})