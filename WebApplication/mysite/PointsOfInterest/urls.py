from django.conf.urls import patterns, url

from PointsOfInterest import views

urlpatterns = patterns('PointsOfInterest',
	url(r'^$', views.index, name='index'),
	#url(r'^place/(?P<placeid>\d+)/$', views.place, name='place'),
	url(r'^place/(?P<placeid>\d+)/$', views.place, name='place'),
	url(r'^(?P<userid>\d+)/places/$', views.places, name='places'),
)
