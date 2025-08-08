from django.urls import path
from . import views

urlpatterns = [
    path('', views.crawler_list, name='crawler_list'),
    path('start_crawl/', views.start_crawl, name='start_crawl'),
    path('jobs/', views.job_list, name='job_list'),
]
