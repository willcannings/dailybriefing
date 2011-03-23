from haystack.indexes import *
from haystack import site
from search.models import Page

class PageIndex(RealTimeSearchIndex):
  text = CharField(document=True, use_template=True)
  first_analysed = DateTimeField(model_attr='first_analysed')
  
  def get_queryset(self):
    return Page.objects.filter(first_analysed__isnull=False)

site.register(Page, PageIndex)
