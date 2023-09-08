from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from django.db.models import Q
from rest_framework import  viewsets
from .news_serializer import NewsSerializer
import requests
import json
from djangophoenix import settings

def paykhalti(request):
    key = settings.env('KEY')
    api_url = settings.env("API_URL")
    url = f"{api_url}"

    payload = json.dumps({
        "return_url": "http://127.0.0.1:8000/",
        "website_url": "http://127.0.0.1:8000/",
        "amount": "1000",
        "purchase_order_id": "Order01",
        "purchase_order_name": "test",
        "customer_info": {
        "name": "Sophia",
        "email": "sophia@gmail.com",
        "phone": "9800000001"
        }
    })
    headers = {
        'Authorization': f'key {key}',
        'Content-Type': 'application/json',
    }

    res = requests.request("POST", url, headers=headers, data=payload)
    return HttpResponse(res.text)







class NewsViews(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer



# Create your views here.
def index(request):
    if request.method == 'POST':
        criteria = request.POST['criteria']
        data={
            'newsData': News.objects.filter(Q(title__icontains=criteria) |
                                             Q(description__icontains=criteria)
                                             | Q(category__name__icontains=criteria)
                                             )
        }
        return render(request,'search.html',data)
    else:
        data={
            'bannerData': News.objects.filter(is_banner=1),
            'newsData': News.objects.filter()
        }
        return render(request,'index.html',data)

def news_details(request,slug):
    obj = News.objects.get(slug=slug)
    obj.page_views += 1
    obj.save()
    data={
        'newsData': News.objects.get(slug=slug),
        'relatedNews': News.objects.all().exclude(slug=slug)
    }
    return render(request,'news.html',data)

def category_news(request,slug):
    data={
        'catData': Category.objects.get(slug=slug),
        'newsData': News.objects.filter(category__slug=slug)
    }
    return render(request,'category.html',data)