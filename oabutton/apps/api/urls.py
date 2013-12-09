from django.conf.urls import patterns, url
from views import add_doc, inspect

urlpatterns = patterns('',
                       # This really need to be moved to the djangorestframework
                       url(r'^add_doc/(?P<secret>.*)/$', add_doc, name="add_doc"),
                       url(r'^inspect/(?P<doi>.*)/$', inspect, name="inspect"),
                       )
