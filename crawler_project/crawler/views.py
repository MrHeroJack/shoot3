import threading
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Crawler, CrawlJob
from .crawlers import run_crawl_in_thread

def crawler_list(request):
    """
    显示所有爬虫的列表，并提供一个表单来启动新的爬取工作。
    """
    crawlers = Crawler.objects.all()
    return render(request, 'crawler/crawler_list.html', {'crawlers': crawlers})

def start_crawl(request):
    """
    启动一个新的爬取工作。
    """
    if request.method == 'POST':
        crawler_id = request.POST.get('crawler_id')
        url = request.POST.get('url')

        if not crawler_id or not url:
            return HttpResponse("Missing crawler_id or URL", status=400)

        crawler = get_object_or_404(Crawler, pk=crawler_id)

        job = CrawlJob.objects.create(
            crawler=crawler,
            status='pending',
            parameters={'url': url}
        )

        thread = threading.Thread(
            target=run_crawl_in_thread,
            args=(job.id,),
            daemon=True
        )
        thread.start()

        return redirect('job_list') # We will create this URL name later

    return redirect('crawler_list')

def job_list(request):
    """
    显示所有爬取工作的列表。
    """
    jobs = CrawlJob.objects.all().order_by('-start_time')
    return render(request, 'crawler/job_list.html', {'jobs': jobs})
