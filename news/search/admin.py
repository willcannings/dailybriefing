from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django import forms
from search.models import *

IMMEDIATE_QUEUE_ANALYSIS_DATE = datetime.datetime(3000,1,1,0,0,0)

def admin_path(name, url):
  return [['/admin', 'admin'], [url, name]]

def admin_sublinks():
  return [['/admin/users', 'users'], ['/admin/sources', 'news sources'], ['/admin/pages', 'page stats']]


# ---------------------------------------------------------
# admin
# ---------------------------------------------------------
@user_passes_test(lambda u: u.is_superuser)
def home(request):
  context = RequestContext(request)
  return render_to_response('admin/home.html', {
    'title': 'Admin',
    'breadcrumbs': [['/admin', 'admin']],
    'sublinks': admin_sublinks()
  }, context_instance=context)


# ---------------------------------------------------------
# users
# ---------------------------------------------------------
class UserForm(forms.Form):
  password = forms.CharField(widget=forms.PasswordInput, max_length=128, required=False)
  confirm = forms.CharField(widget=forms.PasswordInput, max_length=128, required=False)
  admin = forms.BooleanField(required=False)
  
  def clean_confirm(self):
    password = self.cleaned_data.get('password', '')
    confirm = self.cleaned_data['confirm']
    if len(password) != 0 and len(confirm) != 0 and password != confirm:
        raise forms.ValidationError("The password confirmation does not match the password.")
    return confirm


@user_passes_test(lambda u: u.is_superuser)
def users(request):
  users_list = User.objects.all()
  paginator = Paginator(users_list, 25)
  
  try:
    page = int(request.GET.get('page', '1'))
  except ValueError:
    page = 1
    
  try:
    users = paginator.page(page)
  except (EmptyPage, InvalidPage):
    users = paginator.page(paginator.num_pages)
  
  context = RequestContext(request)
  return render_to_response('admin/users.html', {
    'title': 'Users',
    'breadcrumbs': admin_path('users', '/admin/users'),
    'users': users,
    'sublinks': admin_sublinks()
  }, context_instance=context)



@user_passes_test(lambda u: u.is_superuser)
def user(request, id):
  user = get_object_or_404(User, id=id)
  message = ''

  if request.method == 'POST':
    form = UserForm(request.POST)
    if form.is_valid():
      # update the user
      password = form.cleaned_data['password']
      admin = form.cleaned_data['admin']
      
      if len(password) != 0:
        user.set_password(password)
      print "setting to", admin
      user.is_superuser = admin
      user.save()
      message = 'Your changes were successfully saved'
  else:
    form = UserForm(initial={'admin': user.is_superuser})

  context = RequestContext(request)
  return render_to_response('admin/user.html', {
    'title': 'User: ' + user.email,
    'breadcrumbs': admin_path('users', '/admin/users'),
    'user': user,
    'form': form,
    'message': message,
    'sublinks': admin_sublinks()
  }, context_instance=context)


@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, id):
  user = get_object_or_404(User, id=id)

  if request.user.id is not user.id:
    user.delete()
  
  if request.GET.has_key('page'):
    return redirect('/admin/users?page=' + request.GET['page'])
  else:
    return redirect('/admin/users')


# ---------------------------------------------------------
# news sources
# ---------------------------------------------------------
class SourceForm(forms.ModelForm):
  class Meta:
    model = NewsSource
    fields = ('name', 'url_wildcard', 'max_pages', 'l1', 'l2', 't1', 't2', 'a1', 'a2')

class IndexPageForm(forms.ModelForm):
  fields=('url', 'index_page', 'news_source')
  index_page = forms.BooleanField(widget=forms.HiddenInput())
  class Meta: 
    model = Page
# 
# def my_formfield_cb(field): 
#     if isinstance(field, models.FileField) and field.name == 'file': 
#         return fields.FileField(widget = AdminFileWidget(attrs={'url': 
# "/my/url/"})) 
#     return field.formfield() 
# FileFormSet = inlineformset_factory(Version, File, extra=1, 
# formfield_callback = my_formfield_cb) 
# formSet = FileFormSet()

@user_passes_test(lambda u: u.is_superuser)
def sources(request):
  sources_list = NewsSource.objects.all()
  paginator = Paginator(sources_list, 25)
  
  try:
    page = int(request.GET.get('page', '1'))
  except ValueError:
    page = 1
    
  try:
    sources = paginator.page(page)
  except (EmptyPage, InvalidPage):
    sources = paginator.page(paginator.num_pages)
  
  context = RequestContext(request)
  return render_to_response('admin/sources.html', {
    'title': 'Sources',
    'breadcrumbs': admin_path('sources', '/admin/sources'),
    'sources': sources,
    'sublinks': admin_sublinks()
  }, context_instance=context)



@user_passes_test(lambda u: u.is_superuser)
def source(request, id):
  # pages inline formset
  PageFormSet = forms.models.inlineformset_factory(NewsSource, Page, extra=0, form=IndexPageForm, fields=('url', 'index_page', 'news_source'))
  source = get_object_or_404(NewsSource, id=id)
  message = ''

  if request.method == 'POST':
    form = SourceForm(request.POST, instance=source)
    formset = PageFormSet(request.POST, request.FILES, instance=source)
    print formset
    if form.is_valid() and formset.is_valid():
      form.save()
      formset.save()
      message = 'Your changes were successfully saved'
  else:
    form = SourceForm(instance=source)
  
  # re-query for the formset so deleted index pages are removed
  formset = PageFormSet(instance=source, queryset=source.page_set.filter(index_page=True))

  context = RequestContext(request)
  return render_to_response('admin/source.html', {
    'title': 'Source: ' + source.name,
    'breadcrumbs': admin_path('sources', '/admin/sources'),
    'source': source,
    'form': form,
    'formset': formset,
    'message': message,
    'index_count': source.page_set.filter(index_page=True).count(),
    'sublinks': admin_sublinks()
  }, context_instance=context)


@user_passes_test(lambda u: u.is_superuser)
def new_source(request):
  source = NewsSource()
  message = ''

  if request.method == 'POST':
    form = SourceForm(request.POST)
    if form.is_valid():
      source = form.save()
      return redirect('/admin/source/' + str(source.id))
  else:
    form = SourceForm(instance=source)

  context = RequestContext(request)
  return render_to_response('admin/source.html', {
    'title': 'New Source',
    'breadcrumbs': admin_path('sources', '/admin/sources'),
    'form': form,
    'message': message,
    'sublinks': admin_sublinks()
  }, context_instance=context)

@user_passes_test(lambda u: u.is_superuser)
def new_source_index(request, id):
  source = get_object_or_404(NewsSource, id=id)
  new_index = Page()
  new_index.index_page = True
  new_index.news_source = source
  new_index.url = source.url_wildcard
  new_index.next_analysis = IMMEDIATE_QUEUE_ANALYSIS_DATE
  new_index.save()
  return redirect('/admin/source/' + str(source.id))


@user_passes_test(lambda u: u.is_superuser)
def delete_source(request, id):
  source = get_object_or_404(NewsSource, id=id)
  source.delete()
  
  if request.GET.has_key('page'):
    return redirect('/admin/sources?page=' + request.GET['page'])
  else:
    return redirect('/admin/sources')


# ---------------------------------------------------------
# pages
# ---------------------------------------------------------
@user_passes_test(lambda u: u.is_superuser)
def page(request, id):
  page = get_object_or_404(Page, id=id)
  context = RequestContext(request)
  return render_to_response('admin/page.html', {
    'title': 'Page: ' + page.url,
    'breadcrumbs': admin_path('pages', '/admin/pages'),
    'page': page,
    'sublinks': admin_sublinks()
  }, context_instance=context)


@user_passes_test(lambda u: u.is_superuser)
def pages(request):
  pages_list = Page.objects.all()
  paginator = Paginator(pages_list, 25)

  try:
    page = int(request.GET.get('page', '1'))
  except ValueError:
    page = 1

  try:
    pages = paginator.page(page)
  except (EmptyPage, InvalidPage):
    pages = paginator.page(paginator.num_pages)

  context = RequestContext(request)
  return render_to_response('admin/pages.html', {
    'title': 'Pages',
    'breadcrumbs': admin_path('pages', '/admin/pages'),
    'pages': pages,
    'sublinks': admin_sublinks()
  }, context_instance=context)


@user_passes_test(lambda u: u.is_superuser)
def search_pages(request):
  if request.GET.has_key('url'):
    try:
      page = Page.objects.get(url=request.GET['url'])
      return redirect('/admin/page/' + str(page.id))
    except Page.DoesNotExist:
      pass

  context = RequestContext(request)
  return render_to_response('admin/results.html', {
    'title': 'Search Results ',
    'breadcrumbs': admin_path('pages', '/admin/pages'),
    'sublinks': admin_sublinks()
  }, context_instance=context)
