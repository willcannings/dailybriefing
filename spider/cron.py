#!/usr/bin/env python
import datetime
import argparse
import sys
import os

IMMEDIATE_QUEUE_ANALYSIS_DATE = datetime.datetime(3000,1,1,0,0,0)

# the cron task requires a path to the daily briefing django app
parser = argparse.ArgumentParser(description='Daily briefing cron process')
parser.add_argument('--django', required=True, help="path to the django app")
args = parser.parse_args()

# initialise django
sys.path.insert(0, os.path.expanduser(args.django))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from search.models import *

# shift hourly counts to the 24 hour count, and if we're on a
# day boundary, shift all 24 hour counts to the total count.
# also re-sync the queue counts to the actual state of the db.
# because the spider runs with multiple threads, the counts
# can sometimes get a little out of sync.
day_boundary = (datetime.datetime.now().hour == 0)

for news_source in NewsSource.objects.all():
  news_source.last_24_hours += news_source.last_hour
  news_source.last_hour = 0
  if day_boundary:
    news_source.total_indexed += news_source.last_24_hours
    news_source.last_24_hours = 0
  news_source.update_all_counts()
