from django.conf.urls.defaults import *
from django.contrib import admin

urlpatterns = patterns('',
  # users
  url(r'^logout/?', 'django.contrib.auth.views.logout', {'next_page': '/'}, 'logout'),
  url(r'^login/?', 'search.users.new_session'),
  url(r'^signup/?', 'search.users.signup'),
  
  # briefing
  url(r'^briefing/?$', 'search.briefing.index'),
  url(r'^briefing/save_search_items/?', 'search.briefing.save_search_items'),
  
  # settings
  url(r'^settings/?', 'search.users.settings'),
  
  # front end admin
  url(r'^admin/users/?', 'search.admin.users'),
  url(r'^admin/user/(?P<id>\d+)/?', 'search.admin.user'),
  url(r'^admin/delete_user/(?P<id>\d+)/?', 'search.admin.delete_user'),
  url(r'^admin/sources/?$', 'search.admin.sources'),
  url(r'^admin/sources/new/?', 'search.admin.new_source'),
  url(r'^admin/source/(?P<id>\d+)/?', 'search.admin.source'),
  url(r'^admin/new_source_index/(?P<id>\d+)/?', 'search.admin.new_source_index'),
  url(r'^admin/delete_source/(?P<id>\d+)/?', 'search.admin.delete_source'),
  url(r'^admin/pages/search/?', 'search.admin.search_pages'),
  url(r'^admin/pages/?', 'search.admin.pages'),
  url(r'^admin/page/(?P<id>\d+)/?', 'search.admin.page'),
  url(r'^admin/?$', 'search.admin.index'),
  
  # django admin
  (r'^django_admin/doc/', include('django.contrib.admindocs.urls')),
  (r'^django_admin/', include(admin.site.urls)),
  
  # home
  (r'^$', 'search.home.index'),
)
