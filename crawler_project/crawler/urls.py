from django.urls import path
from . import views

# 定义这个应用的URL模式
urlpatterns = [
    # 爬虫列表页面 (主页)
    path('', views.crawler_list, name='crawler_list'),

    # 处理启动新爬取工作的表单提交
    path('start_crawl/', views.start_crawl, name='start_crawl'),

    # 显示所有爬取工作的历史列表
    path('jobs/', views.job_list, name='job_list'),
]
