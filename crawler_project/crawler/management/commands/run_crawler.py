import threading
from django.core.management.base import BaseCommand, CommandError
from crawler.models import Crawler, CrawlJob
from crawler.crawlers import run_crawl_in_thread

class Command(BaseCommand):
    help = 'Starts a crawl job for a given crawler and URL, running it in a background thread.'

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

        # Create the job with a 'pending' status.
        # The thread will update it to 'running'.
        job = CrawlJob.objects.create(
            crawler=crawler,
            status='pending',
            parameters={'url': url}
        )

        self.stdout.write(self.style.SUCCESS(f'Created job {job.id} for crawler "{crawler.name}" with URL: {url}'))

        # Create and start the background thread
        thread = threading.Thread(
            target=run_crawl_in_thread,
            args=(job.id,),
            daemon=True  # Use daemon threads so they exit when the main process exits
        )
        thread.start()

        self.stdout.write(self.style.SUCCESS(f'Job {job.id} started in a background thread.'))
