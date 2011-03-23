from haystack.indexes import *
from haystack import site
from search.models import *

class PageIndex(RealTimeSearchIndex):
  text = CharField(document=True, use_template=True)
  first_analysed = DateTimeField(model_attr='first_analysed')
  a1 = FloatField(model_attr='news_source__a1')
  a2 = FloatField(model_attr='news_source__a2')
  
  def get_queryset(self):
    return Page.objects.filter(first_analysed__isnull=False)

  def get_updated_field(self):
    return 'last_analysed'

  def should_update(self, instance, **kwargs):
    return instance.first_analysed != None

  def prepare(self, obj):
    data = super(PageIndex, self).prepare(obj)
    data['boost'] = obj.static_boost()
    return data

site.register(Page, PageIndex)
