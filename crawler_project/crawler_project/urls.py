"""
URL configuration for crawler_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

# 项目的主URL路由配置
urlpatterns = [
    # Django admin后台
    path("admin/", admin.site.urls),

    # 将所有 /crawler/ 开头的URL都转发到 crawler 应用的 urls.py 文件中进行处理
    path("crawler/", include("crawler.urls")),

    # 将根URL (/) 重定向到爬虫列表页面
    path("", RedirectView.as_view(url="/crawler/", permanent=True)),
]
