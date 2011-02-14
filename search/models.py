from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.db import models

# usernames are email addresses; the default max length of 30 is too short
User._meta.get_field_by_name('username')[0].max_length = 100
User._meta.get_field_by_name('email')[0].max_length = 100

# ---------------------------------------------------------
# models
# ---------------------------------------------------------
class SearchItem(models.Model):
  name            = models.CharField(max_length = 255)
  user            = models.ForeignKey(User)
  category        = models.ForeignKey('SearchCategory')
  created_at      = models.DateTimeField(auto_now_add = True)


class SearchCategory(models.Model):
  name = models.CharField(max_length = 255)
  icon = models.ImageField(upload_to='icons')
  index = models.IntegerField(default = 0)
  
  def items_for_user(self, user):
    return SearchItem.objects.filter(user=user, category=self).order_by('created_at').all()


class NewsSource(models.Model):
  name            = models.CharField(max_length = 255)
  url_wildcard    = models.CharField(max_length = 255)
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


class Page(models.Model):
  index_page      = models.BooleanField(default=False)
  url             = models.CharField(max_length = 255)
  news_source     = models.ForeignKey(NewsSource)
  title           = models.CharField(max_length = 255, default='', blank=True)
  html            = models.TextField(blank=True)
  text            = models.TextField(blank=True)
  first_analysed  = models.DateTimeField(auto_now_add = True)
  last_analysed   = models.DateTimeField(auto_now = True)
  next_analysis   = models.DateTimeField(blank=True, null=True)
  analysis_count  = models.IntegerField(default = 0)
  times_changed   = models.IntegerField(default = 0)
  time_on_index   = models.IntegerField(default = 0)


class Link(models.Model):
  page      = models.ForeignKey(Page, related_name="outbound_set")
  outbound  = models.ForeignKey(Page, related_name="inbound_set")


# ---------------------------------------------------------
# admin
# ---------------------------------------------------------
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
admin.site.unregister(Group)
