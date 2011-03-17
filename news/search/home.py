from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
  if request.session.has_key('error'):
    error = request.session['error']
    del request.session['error']
  else:
    error = ''
  
  if request.GET.has_key('next'):
    next = request.GET['next']
  else:
    next = ''
  
  context = RequestContext(request)
  return render_to_response('home/index.html', {'title': 'Welcome', 'error': error, 'next': next}, context_instance=context)
