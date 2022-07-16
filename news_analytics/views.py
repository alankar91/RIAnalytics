import hashlib
import time

import pandas as pd
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

from RIAnalytics.settings import BASE_DIR
from .forms import *
import os
from .newsInsight import NewsAnalyst

FILES_DIR: str = os.path.join(BASE_DIR, 'files')
# Create your views here.
info = {
    'reportFilename': '',
    'keywordFilename': '',
    'keywords': None,
}


def news_page(request):
    return render(request, 'news_insights.html')


def handle_uploaded_file(f, filename):
    os.makedirs(os.path.dirname(os.path.join(FILES_DIR, filename)), exist_ok=True)
    with open(os.path.join(FILES_DIR, filename), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def news_generate(request):
    analyst = NewsAnalyst()
    print('gotten analyst')
    try:
        print('generating reposer')
        report = analyst.generateHTML(info['reportFilename'], info['keywordFilename'],
                                      namehash=request.GET.get("h", ""))
        print('report done')
        return JsonResponse({'status': 'successful', 'report': report})
    except Exception as E:
        print('Error', str(E))
        return JsonResponse({'status': 'Failed', 'report': ''})


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
        all_files = []
        report_file = request.FILES.getlist('input_files')
        filenames = ""
        if news_form.is_valid():
            print('valid form')
            rfname = ",".join([f.name for f in report_file])
            randnum = int(time.time() / 20)
            nameforhash = f"{rfname}{randnum}"
            namehash = hashlib.md5(nameforhash.encode("utf-8")).hexdigest()
            for f in report_file:
                info['reportFilename'] = f.name
                filenames += f.name
                all_files.append(f.name)
                handle_uploaded_file(f, os.path.join(namehash, f.name))

            keyfile = request.FILES.get('keyword_file')
            info['keywordFilename'] = f"{namehash}.xlsx"
            if keyfile:
                handle_uploaded_file(keyfile, os.path.join(namehash, info['keywordFilename']))
            else:
                info['keywords'] = news_form.cleaned_data['keywords']
                keywords = [k.strip() for k in info['keywords'].split(",")]
                fake_goal = [g.upper() for g in keywords]
                kw_d = {'Key Terms': keywords, 'Goals': fake_goal}
                kw_df = pd.DataFrame(data=kw_d)
                os.makedirs(os.path.dirname(os.path.join(FILES_DIR, namehash, info['keywordFilename'])), exist_ok=True)
                kw_df.to_excel(os.path.join(FILES_DIR, namehash, info['keywordFilename']), index=False)

            if request.is_secure():
                protocol = 'https'
            else:
                protocol = 'http'

            # domain = protocol + "://" + request.META['HTTP_HOST']
            # no need domain to make it confuse, as frontend will follow the domain of visit
            domain = ""

            return render(request, 'news_report.html',
                          context={'mode': 'News', 'files': all_files, 'namehash': namehash, 'url': f'{domain}/news/generate?h={namehash}',
                                   'statusurl': f'{domain}/returnNstatus'})
        else:
            print(news_form.errors)
            return render(request, 'news_insights.html', context={'newsform': news_form})

    return HttpResponseRedirect(reverse('news_mainpage'))
