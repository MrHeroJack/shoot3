from django.core.management.base import BaseCommand, CommandError
from crawler.models import Crawler, CrawlJob
from crawler.crawlers import run_crawl_in_thread

class Command(BaseCommand):
    """
    一个Django management command，用于同步运行一个爬取工作。
    主要用于测试和手动触发。
    """
    help = '为一个给定的爬虫和URL运行一个爬取工作。'

    def add_arguments(self, parser):
        """
        为命令添加命令行参数。
        """
        parser.add_argument('crawler_id', type=int, help='要运行的爬虫的ID')
        parser.add_argument('url', type=str, help='要爬取的URL')

    def handle(self, *args, **options):
        """
        命令的执行逻辑。
        """
        crawler_id = options['crawler_id']
        url = options['url']

        try:
            # 获取指定的爬虫对象
            crawler = Crawler.objects.get(pk=crawler_id)
        except Crawler.DoesNotExist:
            raise CommandError(f'ID为 "{crawler_id}" 的爬虫不存在。')

        # 创建一个新的爬取工作，初始状态为'pending'
        job = CrawlJob.objects.create(
            crawler=crawler,
            status='pending',
            parameters={'url': url}
        )

        self.stdout.write(self.style.SUCCESS(f'已创建工作 {job.id}。正在同步运行...'))

        # 直接调用爬取函数
        run_crawl_in_thread(job.id)

        # 从数据库刷新工作状态以获取最终状态
        job.refresh_from_db()
        self.stdout.write(self.style.SUCCESS(f'工作 {job.id} 已完成，最终状态为: {job.status}'))
