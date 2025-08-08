from django.core.management.base import BaseCommand, CommandError
from crawler.models import Crawler, CrawlJob
from crawler.crawlers import run_crawl_in_thread

class Command(BaseCommand):
    help = 'Runs a crawl job for a given crawler and URL.'

    def add_arguments(self, parser):
        parser.add_argument('crawler_id', type=int, help='The ID of the crawler to run')
        parser.add_argument('url', type=str, help='The URL to crawl')

    def handle(self, *args, **options):
        crawler_id = options['crawler_id']
        url = options['url']

        try:
            crawler = Crawler.objects.get(pk=crawler_id)
        except Crawler.DoesNotExist:
            raise CommandError(f'Crawler with ID "{crawler_id}" does not exist.')

        job = CrawlJob.objects.create(
            crawler=crawler,
            status='pending',
            parameters={'url': url}
        )

        self.stdout.write(self.style.SUCCESS(f'Created job {job.id}. Running synchronously...'))

        # Run the crawl function directly
        run_crawl_in_thread(job.id)

        # Check the final status of the job
        job.refresh_from_db()
        self.stdout.write(self.style.SUCCESS(f'Job {job.id} finished with status: {job.status}'))
