from django.conf.urls import patterns, url

from PointsOfInterest import views

urlpatterns = patterns('PointsOfInterest',
	url(r'^$', views.index, name='index'),
	#url(r'^place/(?P<placeid>\d+)/$', views.place, name='place'),
	url(r'^place/(?P<placeid>\d+)/$', views.place, name='place'),
	url(r'^(?P<userid>\d+)/places/$', views.places, name='places'),
	url(r'^places/$', views.places, name='places'),
	url(r'^friends/$', views.friends, name='friends' ),
	url(r'^settings/$', views.settings, name='settings' ),
	url(r'^createpoi/$', views.createpoi, name='createpoi' ),
	url(r'^login/$', views.logging, name='login' ),
	url(r'^logout/$', views.loggingout, name='logout' ),
)
