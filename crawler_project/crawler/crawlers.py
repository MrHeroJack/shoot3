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
import importlib

def run_crawl_in_thread(job_id):
    """
    在单独的线程中运行爬取工作。
    This version dynamically imports and runs the crawler function.
    """
    job = None
    try:
        job = CrawlJob.objects.get(pk=job_id)
        job.status = 'running'
        job.start_time = timezone.now()
        job.save()

        url = job.parameters.get('url')
        script_path = job.crawler.script_path

        if not script_path:
            raise ValueError("Crawler script_path is not defined.")

        # Dynamically import the crawler function
        module_path, function_name = script_path.rsplit('.', 1)
        module = importlib.import_module(module_path)
        crawler_function = getattr(module, function_name)

        # The Baidu crawler doesn't need a URL, but others might.
        # We can pass the URL as a parameter.
        result_data = crawler_function(url)

        CrawlResult.objects.create(
            job=job,
            url=url,
            data=result_data
        )

        job.status = 'completed'

    except CrawlJob.DoesNotExist:
        print(f"Job {job_id} not found.")
    except Exception as e:
        if job:
            job.status = 'failed'
            CrawlResult.objects.create(
                job=job,
                url=job.parameters.get('url', 'unknown'),
                data={'error': str(e)}
            )
    finally:
        if job:
            job.end_time = timezone.now()
            job.save()


def baidu_hot_search_crawler(url):
    """
    爬取百度热搜榜。
    """
    try:
        # Baidu seems to require a user-agent header
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get("https://top.baidu.com/board?tab=realtime", headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        hot_list = []
        # From browser inspection, the main container for each item is a div with a specific class
        # Let's try to find a more specific selector.
        # The items seem to be in divs with class 'category-wrap_iQLoo'
        items = soup.find_all('div', class_='category-wrap_iQLoo')

        for item in items:
            # The title is in a div with class 't' and a sub-div with class 'title_1Yii5'
            title_div = item.find('div', class_='c-single-text-ellipsis')
            if title_div:
                title = title_div.get_text(strip=True)
                hot_list.append(title)

        return {
            'url': "https://top.baidu.com/board?tab=realtime",
            'hot_list': hot_list
        }

    except requests.RequestException as e:
        return {
            'url': "https://top.baidu.com/board?tab=realtime",
            'error': str(e),
        }
