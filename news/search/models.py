from django.contrib.auth.models import User, Group
from django.contrib import admin
from django.db import models
import datetime
import math

# spider constants
HOUR                    = 60.0
ONE_HOUR                = 60
FIVE_DAYS               = 7200
MAX_FAILURES            = 8
INDEX_ANALYSIS_DELTA    = 15
INITIAL_ANALYSIS_DELTA  = 60
TEXT_MODIFIED_SCALING   = 0.7
TEXT_UNMODIFIED_SCALING = 1.5
IMMEDIATE_QUEUE_ANALYSIS_DATE = datetime.datetime(3000,1,1,0,0,0)

# ---------------------------------------------------------
# models
# ---------------------------------------------------------
class SearchItem(models.Model):
  name            = models.CharField(max_length = 255)
  user            = models.ForeignKey(User)
  category        = models.ForeignKey('SearchCategory')
  created_at      = models.DateTimeField(auto_now_add = True)


# raw queries are used so we can boost result scores with a function
AGE_HOURS = "div(ms(NOW,first_analysed),3600000)"
AGE_BOOST = "product(product(%s,-1),a1)" % AGE_HOURS
FRESHNESS_BOOST = "product(log(sum(div(10,sum(%s,0.001)),1)),a2)" % AGE_HOURS
BOOST_FUNCTION = "sum(%s,%s)" %(AGE_BOOST, FRESHNESS_BOOST)
QUERY_OPTIONS = "{!dismax qf=text pf=text fl=django_ct,django_id,score rows=10 wt=json mm=1 bf=%s}" % BOOST_FUNCTION

class SearchCategory(models.Model):
  name = models.CharField(max_length = 255)
  icon = models.ImageField(upload_to='icons')
  index = models.IntegerField(default = 0)
  
  def items_for_user(self, user):
    return SearchItem.objects.filter(user=user, category=self).order_by('created_at').all()
  
  def results_for_user(self, user):
    query_string = ' '.join([query.name for query in self.items_for_user(user)])
    query = SearchQuerySet().highlight().raw_search("%s%s" % (QUERY_OPTIONS, query_string))
    return query.load_all()
    

class NewsSource(models.Model):
  name            = models.CharField(max_length = 255)
  url_wildcard    = models.CharField(max_length = 1024)
  max_pages       = models.IntegerField(default = 10000, verbose_name="Max pages to process per hour")
  
  # formula variables
  l1              = models.DecimalField(max_digits = 7, decimal_places = 2)
  l2              = models.DecimalField(max_digits = 7, decimal_places = 2)
  t1              = models.DecimalField(max_digits = 7, decimal_places = 2)
  t2              = models.DecimalField(max_digits = 7, decimal_places = 2)
  a1              = models.DecimalField(max_digits = 7, decimal_places = 2)
  a2              = models.DecimalField(max_digits = 7, decimal_places = 2)
  
  # cached index counts
  last_hour       = models.IntegerField(default = 0)
  last_24_hours   = models.IntegerField(default = 0)
  total_indexed   = models.IntegerField(default = 0)
  
  # cached queue counts
  queue_immediate = models.IntegerField(default = 0)
  delayed_total   = models.IntegerField(default = 0)
  delayed_ready   = models.IntegerField(default = 0)
  
  def indexed_last_hour(self):
    return self.last_hour
  
  def indexed_last_day(self):
    return self.last_hour + self.last_24_hours
  
  def indexed_all_time(self):
    return self.last_hour + self.last_24_hours + self.total_indexed
  
  def update_ready_count(self):
    self.delayed_ready = self.page_set.filter(next_analysis__lte=datetime.datetime.now()).count()
    self.save()
  
  def update_all_counts(self):
    self.queue_immediate = self.page_set.filter(next_analysis=IMMEDIATE_QUEUE_ANALYSIS_DATE).count()
    self.delayed_total = self.page_set.filter(next_analysis__isnull=False).count() - self.queue_immediate
    self.update_ready_count()


class Page(models.Model):
  index_page      = models.BooleanField(default=False)
  url             = models.CharField(max_length = 1024)
  news_source     = models.ForeignKey(NewsSource)
  title           = models.CharField(max_length = 1024, default='', blank=True)
  text            = models.TextField(blank=True)
  first_analysed  = models.DateTimeField(blank=True, null=True)
  last_analysed   = models.DateTimeField(blank=True, null=True)
  next_analysis   = models.DateTimeField(blank=True, null=True)
  analysis_delta  = models.IntegerField(default = 60)
  analysis_count  = models.IntegerField(default = 0)
  times_changed   = models.IntegerField(default = 0)
  time_on_index   = models.IntegerField(default = 0)
  failure_count   = models.IntegerField(default = 0)
  
  def static_boost(self):
    inbound_boost = math.log(((self.inbound_set.count() - 1) * float(self.news_source.l1)) + 1) * float(self.news_source.l2)
    index_boost = math.log(((self.time_on_index / HOUR) * float(self.news_source.t1)) + 1) * float(self.news_source.t2)
    return inbound_boost + index_boost
  
  def error(self):
    self.failure_count += 1
    if self.failure_count == MAX_FAILURES:
      if self.first_analysed != None:
        self.news_source.delayed_total -= 1
        self.news_source.save()
      self.delete()
    else:
      self.next_analysis = datetime.datetime.now() + datetime.timedelta(minutes=5*(2 ** (self.failure_count - 1)))
      self.news_source.save()
      self.save()
  
  def complete(self, text):
    # update analysis times
    analysis_time = datetime.datetime.now()
    self.last_analysed = analysis_time
    if self.first_analysed == None:
      self.first_analysed = analysis_time
    
    # analysis was successful
    self.failure_count = 0
    self.analysis_count += 1
    
    # update the analysis delta and associated next analysis
    if self.index_page:
      self.analysis_delta = INDEX_ANALYSIS_DELTA
    else:
      if self.analysis_count == 1:
        self.news_source.queue_immediate -= 1
        self.news_source.delayed_total += 1
        self.analysis_delta = INITIAL_ANALYSIS_DELTA
        self.text = text
      else:
        if text != self.text:
          self.analysis_delta = max(self.analysis_delta * TEXT_MODIFIED_SCALING, ONE_HOUR)
          self.times_changed += 1
          self.text = text
        else:
          self.analysis_delta = min(self.analysis_delta * TEXT_UNMODIFIED_SCALING, FIVE_DAYS)
    
    # pages become stale after 5 days
    five_days_ago = datetime.datetime.now() - datetime.timedelta(days=5)
    if self.first_analysed <= five_days_ago and not self.index_page:
      self.news_source.delayed_total -= 1
      self.next_analysis = None
    else:
      self.next_analysis = datetime.datetime.now() + datetime.timedelta(minutes=self.analysis_delta)    
    self.save()
    
    # update the news source analysis counts; a cron task moves the hourly count to daily, to total and so on
    self.news_source.last_hour += 1
    self.news_source.save()


class Link(models.Model):
  page      = models.ForeignKey(Page, related_name="outbound_set")
  outbound  = models.ForeignKey(Page, related_name="inbound_set")


# ---------------------------------------------------------
# admin
# ---------------------------------------------------------
# usernames are email addresses; the default max length of 30 is too short
User._meta.get_field_by_name('username')[0].max_length = 100
User._meta.get_field_by_name('email')[0].max_length = 100

class SearchCategoryAdmin(admin.ModelAdmin):
  list_display = ('name',)
  ordering = ('index',)


class NewsSourceAdmin(admin.ModelAdmin):
  list_display = ('name',)
  search_fields = ['name']
  fieldsets = (
    (None, {
      'fields': ('name',)
    }),
    ('Pages Indexed', {
      'fields': ('last_hour', 'last_24_hours', 'total_indexed')
    }),
    ('Queues', {
      'fields': ('queue_immediate', 'delayed_total', 'delayed_ready')
    }),
    ('Options', {
      'classes': ('collapse',),
      'fields': ('url_wildcard', 'max_pages', 'l1', 'l2', 't1', 't2', 'a1', 'a2')
    })
  )

class PageAdmin(admin.ModelAdmin):
  pass

admin.site.register(SearchCategory, SearchCategoryAdmin)
admin.site.register(NewsSource, NewsSourceAdmin)
admin.site.register(Page, PageAdmin)

from haystack.query import SearchQuerySet
