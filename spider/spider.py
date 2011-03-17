#!/usr/bin/env python
import argparse
import logging
import signal
import time
import sys
import os

SLEEP_DURATION = 60

# ---------------------------------------------------------
# Initialisation
# ---------------------------------------------------------
# the spider requires a path to the daily briefing django app
parser = argparse.ArgumentParser(description='Daily briefing spider process')
parser.add_argument('--workers', default=2, type=int, help="number of worker threads to start (defaults to 2)")
parser.add_argument('--django', required=True, help="path to the django app")
args = parser.parse_args()

# initialise logging
logger          = logging.getLogger('spider')
file_handler    = logging.FileHandler('/var/log/spider.log')
stderr_handler  = logging.StreamHandler()
formatter       = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
file_handler.setFormatter(formatter)
stderr_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stderr_handler)
logger.setLevel(logging.DEBUG)


# ---------------------------------------------------------
# Boot
# ---------------------------------------------------------
# initialise with django and modules
logger.info("Starting up...")
sys.path.insert(0, os.path.expanduser(args.django))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from page_queue import PageQueue
from worker import Worker
queue = PageQueue(logger)
workers = []
running = True

# create the worker threads
for i in range(args.workers):
  new_worker = Worker(queue, logger)
  workers.append(new_worker)
  new_worker.start()

# install the shutdown signal handler
def shutdown_spider(signum, frame):
  global running, logger, workers
  logger.info("Shutting down...")
  running = False
  for worker in workers:
    worker.running = False

signal.signal(signal.SIGINT, shutdown_spider)
signal.signal(signal.SIGHUP, shutdown_spider)
signal.signal(signal.SIGTERM, shutdown_spider)


# ---------------------------------------------------------
# Runtime
# ---------------------------------------------------------
# run loop; every SLEEP_DURATION seconds poll the database for queue changes
while running:
  queue.pull_from_database()
  time.sleep(SLEEP_DURATION)
