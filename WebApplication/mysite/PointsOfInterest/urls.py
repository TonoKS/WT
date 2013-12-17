from django.conf.urls import patterns, url
from PointsOfInterest import views

urlpatterns = patterns('PointsOfInterest',
	url(r'^$', views.index, name='index'),
	url(r'^place/(?P<placeid>\d+)/$', views.place, name='place'),
	url(r'^place/(?P<placeid>\d+)/edit/$', views.poiedit, name='poiedit'),
	url(r'^place/(?P<placeid>\d+)/del/$', views.poidel, name='poidel'),
	url(r'^mypoints/$', views.mypoints, name='mypoints'),
	url(r'^mypoints/bigmap/$', views.mybigmap, name='mybigmap'),
	url(r'^myfriends/$', views.myfriends, name='myfriends'),
	url(r'^users/(?P<username>\w+)/$', views.user, name='user'),
	url(r'^users/(?P<username>\w+)/confirm/$', views.fsconfirm, name='fsconfirm'),
	url(r'^users/(?P<username>\w+)/send/$', views.fssend, name='fssend'),
	url(r'^users/(?P<username>\w+)/cancel/$', views.fscancel, name='fscancel'),
	url(r'^users/(?P<username>\w+)/bigmap/$', views.userbigmap, name='userbigmap'),
	url(r'^createpoi/$', views.createpoi, name='createpoi'),
	url(r'^login/$', views.logging, name='login' ),
	url(r'^logout/$', views.loggingout, name='logout'),
	url(r'^find/$', views.find, name='find'),
	url(r'^registration/$', views.registration, name='registration'),
	url(r'^delcomm/(?P<commid>\d+)/$', views.delcomm, name='delcomm'),
)
