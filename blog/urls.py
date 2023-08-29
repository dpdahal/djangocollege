from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('news/<slug>',views.news_details,name='news'),
    path('category/<slug>',views.category_news,name='category'),
]
