from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from search.models import *

@login_required
def index(request):
  categories = [[x, x.items_for_user(request.user)] for x in SearchCategory.objects.order_by('index').all()]
  context = RequestContext(request)
  return render_to_response('briefing/index.html', {'title': 'Your Briefing', 'categories': categories}, context_instance=context)


@login_required
def save_search_items(request):
  if request.POST.has_key('category_id'):
    # delete any existing search items for this category
    category = get_object_or_404(SearchCategory, id=request.POST['category_id'])
    SearchItem.objects.filter(user=request.user, category=category).delete()
    
    # create the search items
    for i in range(1,11):
      field = 'q' + str(i)
      if request.POST.has_key(field) and request.POST[field] != '':
        item = SearchItem()
        item.category = category
        item.user = request.user
        item.name = request.POST[field]
        item.save()
    
  return redirect('/briefing')
