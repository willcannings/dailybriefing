from haystack.indexes import *
from haystack import site
from search.models import *

class PageIndex(SearchIndex):
  text = CharField(document=True, use_template=True)
  first_analysed = DateTimeField(model_attr='first_analysed')
  
  def get_queryset(self):
    return Page.objects.filter(first_analysed__isnull=False)

  def should_update(self, instance, **kwargs):
    return instance.first_analysed != None

  def prepare(self, obj):
    data = super(PageIndex, self).prepare(obj)
    data['boost'] = obj.static_boost()
    return data

site.register(Page, PageIndex)
