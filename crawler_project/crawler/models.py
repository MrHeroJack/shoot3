from django.db import models

class Crawler(models.Model):
    """
    爬虫模型
    """
    name = models.CharField(max_length=255, verbose_name="爬虫名称")
    description = models.TextField(blank=True, null=True, verbose_name="爬虫描述")
    script_path = models.CharField(max_length=255, verbose_name="脚本路径")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "爬虫"
        verbose_name_plural = verbose_name

class CrawlJob(models.Model):
    """
    爬取工作模型
    """
    STATUS_CHOICES = (
        ('pending', '待处理'),
        ('running', '运行中'),
        ('completed', '已完成'),
        ('failed', '已失败'),
    )
    crawler = models.ForeignKey(Crawler, on_delete=models.CASCADE, verbose_name="爬虫")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="状态")
    start_time = models.DateTimeField(null=True, blank=True, verbose_name="开始时间")
    end_time = models.DateTimeField(null=True, blank=True, verbose_name="结束时间")
    parameters = models.JSONField(default=dict, blank=True, verbose_name="参数")

    def __str__(self):
        return f"{self.crawler.name} - {self.get_status_display()} - {self.start_time}"

    class Meta:
        verbose_name = "爬取工作"
        verbose_name_plural = verbose_name

class CrawlResult(models.Model):
    """
    爬取结果模型
    """
    job = models.ForeignKey(CrawlJob, on_delete=models.CASCADE, verbose_name="爬取工作")
    url = models.URLField(max_length=1024, verbose_name="URL")
    data = models.JSONField(verbose_name="提取的数据")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return f"{self.job} - {self.url}"

    class Meta:
        verbose_name = "爬取结果"
        verbose_name_plural = verbose_name
