from django.conf.urls import patterns, url
from views import add_doc

urlpatterns = patterns('',
                       # This really need to be moved to the djangorestframework
                       url(r'^add_doc/(?P<secret>.*)/$', add_doc, name="add_doc"),
                       )
