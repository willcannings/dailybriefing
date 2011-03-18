from django.db.models import Q
from search.models import *
import threading
import datetime
import urlparse
import Queue
import re

TIMEOUT_SECONDS       = 1
INDEX_ANALYSIS_DELTA  = 15
IMMEDIATE_QUEUE_ANALYSIS_DATE = datetime.datetime(3000,1,1,0,0,0)

class PageQueue:
  def __init__(self, logger):
    self.logger = logger
    self.pages = {}
    self.queue = Queue.PriorityQueue()
    self.mutex = threading.Lock()
  
  # the database stores the list of all pages and their next analysis
  # datetimes. we query the database for the list of all pages that
  # /should/ be in the queue right now, and add any we haven't yet
  # seen. once a page has been processed, its next_analysis field is
  # set to a time in the future, and we don't need to store or track
  # the page until that time.
  def pull_from_database(self):
    self.logger.debug("Pulling queue from database")
    pages = Page.objects.filter(Q(next_analysis__lte=datetime.datetime.now) | Q(next_analysis=IMMEDIATE_QUEUE_ANALYSIS_DATE)).order_by('next_analysis').all()
    self.logger.debug("Found " + str(len(pages)) + " pages")
    
    self.mutex.acquire()
    added = 0
    for page in pages:
      if page.url not in self.pages:
        added += 1
        self.queue.put((page.next_analysis, page))
        self.pages[page.url] = page
    self.mutex.release()
    self.logger.info("Added " + str(added) + " new pages from the database")
    
    self.logger.debug("Updating news source ready counts")
    for source in NewsSource.objects.all():
      source.update_ready_count()
  
  
  def add_pages(self, links, page):
    seen = {}
    
    for link in links:
      components = urlparse.urlsplit(urlparse.urljoin(page.url, link.attrib['href']))
      url = urlparse.urlunsplit((components.scheme, components.netloc, components.path, '', ''))
      if url in seen:
        continue
      else:
        seen[url] = 1
      linked_page = None
      
      if url in self.pages:
        linked_page = self.pages[url]
      else:
        try:
          linked_page = Page.objects.get(url=url)
        except Page.DoesNotExist:
          linked_page = self.create_page(url)
      
      # only continue if the url matches an existing page, or matches a news url source wildcard
      if linked_page == None:
        continue
      
      # create a link between the two pages if necessary
      if not Link.objects.filter(page=page, outbound=linked_page).exists():
        link = Link()
        link.page = page
        link.outbound = linked_page
        link.save()
      
      # index pages are analysed every n minutes; if a page is present on an index page, it has been present for at most n minutes since the last analysis
      if page.index_page and not linked_page.index_page:
        linked_page.time_on_index += INDEX_ANALYSIS_DELTA
        linked_page.save()


  def create_page(self, url):
    # pages must belong to a news source and match a url wildcard
    for source in NewsSource.objects.all():
      regex = re.compile(source.url_wildcard.replace('*', '.*'))
      if regex.match(url):
        news_source = source
        break
    else:
      return None
    
    # create a new page
    self.logger.debug("Adding new page: " + url)
    page = Page()
    page.next_analysis = IMMEDIATE_QUEUE_ANALYSIS_DATE
    page.news_source = news_source
    page.url = url
    page.save()
    
    news_source.queue_immediate += 1
    news_source.save()
    
    # add to the queue immediately if appropriate
    self.mutex.acquire()
    if url not in self.pages:
      self.queue.put((page.next_analysis, page))
      self.pages[page.url] = page
    self.mutex.release()
    return page

  
  # retrieve a page off the queue with a timeout so the thread can check its
  # running flag every TIMEOUT_SECONDS and die for safe shutdown
  def get_page(self):
    # FIXME: ensure max pages per hour per news source is honoured
    try:
      item = self.queue.get(True, TIMEOUT_SECONDS)
      return item[1]
    except Queue.Empty:
      return None

  def remove_page(self, page):
    self.mutex.acquire()
    del self.pages[page.url]
    self.mutex.release()
