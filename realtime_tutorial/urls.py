from django.conf.urls import patterns, include, url
from django.contrib import admin
urlpatterns = patterns('',
    url(r'^$', 'core.views.home', name='home'),
    url(r'^node_api$', 'core.views.node_api', name='node_api'),
    url(r'^register/$', 'core.views.register', name='register'),
     url(r'^logout/$', 'core.views.logout_user', name='logout'),
      url(r'^login/$', 'core.views.login_user', name='login'),
    
#     url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}, name='login'),
 
    url(r'^admin/', include(admin.site.urls)),
)
