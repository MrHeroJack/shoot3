import requests
from bs4 import BeautifulSoup

def simple_crawler(url):
    """
    一个简单的爬虫，用于获取给定URL的标题。
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # 如果请求失败则引发HTTPError

        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('title').get_text(strip=True) if soup.find('title') else 'No title found'

        return {
            'url': url,
            'title': title,
        }
    except requests.RequestException as e:
        return {
            'url': url,
            'error': str(e),
        }

from .models import CrawlJob, CrawlResult
from django.utils import timezone

def run_crawl_in_thread(job_id):
    """
    在单独的线程中运行爬取工作。
    """
    try:
        job = CrawlJob.objects.get(pk=job_id)
        job.status = 'running'
        job.start_time = timezone.now()
        job.save()

        url = job.parameters.get('url')
        if not url:
            raise ValueError("URL not found in job parameters")

        result_data = simple_crawler(url)

        CrawlResult.objects.create(
            job=job,
            url=url,
            data=result_data
        )

        job.status = 'completed'

    except CrawlJob.DoesNotExist:
        # The job was deleted before the thread could run.
        # Log this or handle it as needed.
        print(f"Job {job_id} not found.")
    except Exception as e:
        if 'job' in locals():
            job.status = 'failed'
            CrawlResult.objects.create(
                job=job,
                url=job.parameters.get('url', 'unknown'),
                data={'error': str(e)}
            )
    finally:
        if 'job' in locals() and job is not None:
            job.end_time = timezone.now()
            job.save()
