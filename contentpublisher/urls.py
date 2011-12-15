'''
Created on 15 Dec 2011

@author: euan
'''
from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required

from django.views import generic as generic_views

from django.contrib import admin
admin.autodiscover()

from contentpublisher import models

urlpatterns = patterns('contentpublisher.views',
                       
    url(r'^$',
        login_required(generic_views.ListView.as_view(queryset=models.ContentUpgrade.objects.all(),
                                                      template_name='contentpublisher/content_list.html')
                       ),
        name='content_publisher_content_list'),
        
)