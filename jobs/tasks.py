from celery import shared_task
from .scraper import scrape_myjobmag

@shared_task
def run_myjobmag_scraper():
    """Celery task to run the MyJobMag scraper."""
    scrape_myjobmag()
