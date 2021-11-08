#Standard lib
from datetime import timezone
import logging
#Django
from django.conf import settings
from django.core.management.base import BaseCommand
#Third party
import feedparser
from dateutil import parser
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
#Models
from podcasts.models import Episode

logger = logging.getLogger(__name__)

def save_episodes(link):
        feed = feedparser.parse(link)
        pod_title = feed.channel.title
        pod_img = feed.channel.image['href']
        
        for i in feed.entries:
            
            if not Episode.objects.filter(guid=i.guid).exists():
                episode = Episode(
                    title = i.title,
                    description = i.description,
                    pub_date = parser.parse(i.published),
                    link = i.link,
                    img_url = pod_img,
                    podcast_name = pod_title,
                    guid = i.guid
                )
                episode.save()
def get_realpython_episodes():
    save_episodes('https://realpython.com/podcasts/rpp/feed')
    print('Hola')
    
def save_spreker():
    save_episodes('https://blog.feedspot.com/podcast_rss_feeds/')
def delete_old_job_execution(max_age = 604_800):
     DjangoJobExecution.objects.delete_old_job_execution(max_age)

class Command(BaseCommand):
    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(),'default')
        scheduler.add_job(
            get_realpython_episodes,
            trigger='interval',
            minutes=2,
            id = 'The Real Python Podcast',
            max_instances=1,
            replace_existing=True
        )
        logger.info("Added job: The Real Python Podcast.")
        scheduler.add_job(
            delete_old_job_execution,
            trigger=CronTrigger(day_of_week='mon',hour=00,minute=00),
            id = 'Delete old executions',
            max_instances=1,
            replace_existing=True
        )
        logger.info('Added weekly job : Delete old executions')
        
        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
        
    
        
    