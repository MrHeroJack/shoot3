from django.contrib import admin
from .models import Crawler, CrawlJob, CrawlResult

@admin.register(Crawler)
class CrawlerAdmin(admin.ModelAdmin):
    """
    爬虫管理界面
    """
    list_display = ('name', 'script_path', 'created_at', 'updated_at')
    search_fields = ('name', 'description')

@admin.register(CrawlJob)
class CrawlJobAdmin(admin.ModelAdmin):
    """
    爬取工作管理界面
    """
    list_display = ('crawler', 'status', 'start_time', 'end_time')
    list_filter = ('status',)
    search_fields = ('crawler__name',)

@admin.register(CrawlResult)
class CrawlResultAdmin(admin.ModelAdmin):
    """
    爬取结果管理界面
    """
    list_display = ('job', 'url', 'created_at')
    search_fields = ('url',)
    # For performance, we don't show the full data in the list view
    # raw_id_fields = ('job',) # This can be useful for large numbers of jobs
