from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from datetime import datetime 



from PointsOfInterest.models import PointOfInterest
from PointsOfInterest.models import Friend
from PointsOfInterest.models import Commentary
from PointsOfInterest.models import CreatePoiForm
from PointsOfInterest.models import LoginForm
from PointsOfInterest.models import RegistrationForm
from PointsOfInterest.models import CommentaryForm
from PointsOfInterest.models import FindForm



@login_required(login_url='/POI/login/')
def index(request):
	return HttpResponse("Hello, world. You're at our exciting site about Points of Interest")

def loggingout(request):
	logout(request)
	return HttpResponseRedirect('/POI/login/')


def logging(request):
	#request.session['test'] = 'test'
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					template = loader.get_template('PointsOfInterest/login.html')
					context = RequestContext(request, { })
					return HttpResponse(template.render(context))
				else:
					return HttpResponse("Ucet neaktivny")
		else:
			form = LoginForm(request.POST)
			template = loader.get_template('PointsOfInterest/login.html')
			context = RequestContext(request, {
				'form' : form,
				})
			return HttpResponse(template.render(context))
	else:
		form = LoginForm()
		template = loader.get_template('PointsOfInterest/login.html')
		context = RequestContext(request, {
			'form' : form,
			})
		return HttpResponse(template.render(context))


def place(request, placeid):
	place = PointOfInterest.objects.get(id = placeid)
	comments = Commentary.objects.filter(poiid = place.id).order_by('-dateCreated')
	if request.user:
		friendship = Friend.objects.filter(who = request.user.id, fwith = place.userid.id,  confirmed = True)
		if not friendship:
			friendship = Friend.objects.filter(who = place.userid.id, fwith = request.user.id, confirmed = True)
	if (friendship and place.category == 'f') or place.category == 'o' or place.userid == request.user:
		if request.method == 'POST':
			form = CommentaryForm(request.POST)
			if form.is_valid():
				commentary = Commentary()
				commentary.userid = request.user
				commentary.poiid = place
				commentary.commentary = form.cleaned_data['commentary']
				commentary.dateCreated = datetime.now()
				commentary.save()
				form = CommentaryForm()
				template = loader.get_template('PointsOfInterest/place.html')
				context = RequestContext(request, {
					'place' : place,
					'form' : form,
					'comments' : comments,
					})
				return HttpResponse(template.render(context))
			else:
				template = loader.get_template('PointsOfInterest/place.html')
				context = RequestContext(request, {
					'place': place,
					'form' : form,
					'comments' : comments,
					})
				return HttpResponse(template.render(context))
		else:
			form = CommentaryForm()
			template = loader.get_template('PointsOfInterest/place.html')
			context = RequestContext(request, {
				'place': place,
				'form' : form,
				'comments' : comments,
				})
			return HttpResponse(template.render(context))
	else:
		template = loader.get_template('PointsOfInterest/error.html')
		context = RequestContext(request, {
			'err' : 9,
			})
		return HttpResponse(template.render(context))

@login_required(login_url='/POI/login/')
def mypoints(request):
	places = PointOfInterest.objects.filter(userid = User.objects.get(id = request.user.id)).order_by('title')
	template = loader.get_template('PointsOfInterest/places.html')
	context = RequestContext(request, {
        'places': places,
        })
	return HttpResponse(template.render(context))

@login_required(login_url='/POI/login/')
def places(request, userid):
	template = loader.get_template('PointsOfInterest/places.html')
	context = RequestContext(request, {
        'places': places,
        })
	return HttpResponse(template.render(context))


@login_required(login_url='/POI/login/')
def createpoi(request):
	if request.method == 'POST':
		form = CreatePoiForm(request.POST)
		if form.is_valid():
			place = PointOfInterest()
			place.userid = request.user
			place.title = form.cleaned_data['title']
			place.description = form.cleaned_data['description']
			place.latitude = form.cleaned_data['latitude']
			place.longitude = form.cleaned_data['longitude']
			place.category = form.cleaned_data['category']
			place.dateCreated = datetime.now()
			place.dateModified = None
			place.save()
			return HttpResponseRedirect('/POI/place/'+str(place.id)+'/')
		else:
			form = CreatePoiForm(request.POST)
			template = loader.get_template('PointsOfInterest/createpoi.html')
			context = RequestContext(request, {
				'form' : form,
			})
			return HttpResponse(template.render(context))
	else:
		form = CreatePoiForm()
		template = loader.get_template('PointsOfInterest/createpoi.html')
		context = RequestContext(request, {
			'form': form,
		})
		return HttpResponse(template.render(context))
		
		
		"""now = datetime.datetime.now()
	html = "<html><body>It is now %s . %d . %d</body></html>" % (place.title, place.id, request.user.id)
	return HttpResponse(html)"""
		
		
@login_required(login_url='/POI/login/')
def poiedit(request, placeid):
	place = PointOfInterest.objects.get(id = placeid)
	if User.objects.get(id = request.user.id) == place.userid:
		if request.method == 'POST':
			form = CreatePoiForm(request.POST)
			if form.is_valid():
				place.userid = request.user
				place.title = form.cleaned_data['title']
				place.description = form.cleaned_data['description']
				place.latitude = form.cleaned_data['latitude']

				place.longitude = form.cleaned_data['longitude']
				place.category = form.cleaned_data['category']
				place.dateModified = datetime.now()
				place.save()
				return HttpResponseRedirect('/POI/place/'+str(place.id)+'/')
				return HttpResponse(template.render(context))
			else:
				form = CreatePoiForm(request.POST)
				template = loader.get_template('PointsOfInterest/poiedit.html')
				context = RequestContext(request, {
					'form' : form,
					'place' : place,
				})
				return HttpResponse(template.render(context))
		else:
			form = CreatePoiForm(initial={'title': place.title, 'description': place.description, 'latitude': place.latitude, 'longitude': place.longitude, 'category' : place.category})
			template = loader.get_template('PointsOfInterest/poiedit.html')
			context = RequestContext(request, {
				'form' : form,
				'place' : place,
			})
			return HttpResponse(template.render(context))
	else:
		template = loader.get_template('PointsOfInterest/error.html')
		context = RequestContext(request, {
				'err': 1,
			})
		return HttpResponse(template.render(context))


@login_required(login_url='/POI/login/')
def poidel(request, placeid):
	place = PointOfInterest.objects.get(id = placeid)
	if User.objects.get(id = request.user.id) == place.userid:	
		if request.method == 'POST':
			form = CreatePoiForm(request.POST)
			place.delete()
			return HttpResponseRedirect('/POI/mypoints/')
			return HttpResponse(template.render(context))
		else:
			template = loader.get_template('PointsOfInterest/question.html')
			context = RequestContext(request, {
				 'place' : place, 'qst' : 1,
			})
			return HttpResponse(template.render(context))
	else:
		template = loader.get_template('PointsOfInterest/error.html')
		context = RequestContext(request, {
				'err': 1,
			})
		return HttpResponse(template.render(context))


def myfriends(request):
	#conf1 = Friend.objects.filter(who = request.user).filter(confirmed=True)
	conf1 = Friend.objects.filter(who = request.user).filter(confirmed=True)
	conf2 = Friend.objects.filter(fwith = request.user).filter(confirmed=True)
	confirmed = conf1 | conf2
	sentunconf = Friend.objects.filter(who = request.user).filter(confirmed=False)
	rcvtunconf = Friend.objects.filter(fwith = request.user).filter(confirmed=False)

	template = loader.get_template('PointsOfInterest/friends.html')
	context = RequestContext(request, {
		'confirmed' : confirmed,
		'sentunconf' : sentunconf,
		'rcvtunconf' : rcvtunconf,
			})
	return HttpResponse(template.render(context))
	
	
	#isrequested and issent
def user(request, username):
	uuser = User.objects.get(username = username)
	if uuser == request.user:
		return HttpResponseRedirect('/POI/mypoints/')
	isconfirmed = False
	issent = False
	isreceived = False
	if request.user.is_authenticated:
		friendship = Friend.objects.filter(who = request.user.id, fwith = uuser.id, confirmed = True)
		if not friendship:
			friendship = Friend.objects.filter(who = uuser.id, fwith = request.user.id, confirmed = True)
		if friendship:
			isconfirmed = True
		friendship = Friend.objects.filter(who = request.user.id, fwith = uuser.id, confirmed = False)
		if friendship:
			issent = True
		friendship = Friend.objects.filter(who = uuser.id, fwith = request.user.id, confirmed = False)
		if friendship:
			isreceived = True
	points1 = PointOfInterest.objects.filter(userid = uuser).filter(category = 'o')
	if isconfirmed:
		points2 = PointOfInterest.objects.filter(userid = uuser).filter(category = 'f')
		points = points1 | points2
	else:
		points = points1
	points = points.order_by('title')
	template = loader.get_template('PointsOfInterest/user.html')
	context = RequestContext(request, {
		'uuser' : uuser,
		'points' : points,
		'isconfirmed' : isconfirmed,
		'issent' : issent,
		'isreceived' : isreceived,
			})
	return HttpResponse(template.render(context))



@login_required(login_url='/POI/login/')
def fsconfirm(request, username):
	uuser = User.objects.get(username = username)
	if uuser == request.user:
		return HttpResponseRedirect('/POI/mypoints/')
	isconfirmed = False
	issent = False
	isreceived = False
	if request.user:
		friendship = Friend.objects.filter(who = request.user, fwith = uuser, confirmed = True)
		if not friendship:
			friendship = Friend.objects.filter(who = uuser, fwith = request.user, confirmed = True)
		if friendship:
			isconfirmed = True
		friendship = Friend.objects.filter(who = request.user, fwith = uuser, confirmed = False)
		if friendship:
			issent = True
		friendship = Friend.objects.filter(who = uuser, fwith = request.user, confirmed = False)
		if friendship:
			isreceived = True
			
		if isreceived:
			if request.method == 'POST':
				friendship = Friend.objects.get(who = uuser, fwith = request.user, confirmed = False)
				friendship.dateCreated = datetime.now()
				friendship.confirmed = True
				friendship.save()
				return HttpResponseRedirect('/POI/users/'+str(uuser.username)+'/')
			else:
				template = loader.get_template('PointsOfInterest/question.html')
				context = RequestContext(request, {
					 'uuser' : uuser, 'qst' : 2,
				})
				return HttpResponse(template.render(context))
		elif issent:
			template = loader.get_template('PointsOfInterest/error.html')
			context = RequestContext(request, {
					'err': 3,
				})
			return HttpResponse(template.render(context))
		elif isconfirmed:
			template = loader.get_template('PointsOfInterest/error.html')
			context = RequestContext(request, {
					'err': 4,
				})
			return HttpResponse(template.render(context))
		else:
			template = loader.get_template('PointsOfInterest/error.html')
			context = RequestContext(request, {
					'err': 0,
				})
			return HttpResponse(template.render(context))



@login_required(login_url='/POI/login/')
def fssend(request, username):
	uuser = User.objects.get(username = username)
	if uuser == request.user:
		return HttpResponseRedirect('/POI/mypoints/')
	isconfirmed = False
	issent = False
	isreceived = False
	if request.user:
		friendship = Friend.objects.filter(who = request.user, fwith = uuser, confirmed = True)
		if not friendship:
			friendship = Friend.objects.filter(who = uuser, fwith = request.user, confirmed = True)
		if friendship:
			isconfirmed = True
		friendship = Friend.objects.filter(who = request.user, fwith = uuser, confirmed = False)
		if friendship:
			issent = True
		friendship = Friend.objects.filter(who = uuser, fwith = request.user, confirmed = False)
		if friendship:
			isreceived = True
			
		if not (isconfirmed and issent and isreceived):
			if request.method == 'POST':
				friendship = Friend()
				friendship.who = request.user
				friendship.fwith = uuser
				friendship.dateCreated = datetime.now()
				friendship.confirmed = False
				friendship.save()
				return HttpResponseRedirect('/POI/users/'+str(uuser.username)+'/')
			else:
				template = loader.get_template('PointsOfInterest/question.html')
				context = RequestContext(request, {
					 'uuser' : uuser, 'qst' : 3,
				})
				return HttpResponse(template.render(context))
		elif issent:
			template = loader.get_template('PointsOfInterest/error.html')
			context = RequestContext(request, {
					'err': 5,
				})
			return HttpResponse(template.render(context))
		elif isconfirmed:
			template = loader.get_template('PointsOfInterest/error.html')
			context = RequestContext(request, {
					'err': 4,
				})
			return HttpResponse(template.render(context))
		elif received:
			template = loader.get_template('PointsOfInterest/error.html')
			context = RequestContext(request, {
					'err': 6,
				})
			return HttpResponse(template.render(context))
		else:
			template = loader.get_template('PointsOfInterest/error.html')
			context = RequestContext(request, {
					'err': 0,
				})
			return HttpResponse(template.render(context))




@login_required(login_url='/POI/login/')
def fscancel(request, username):
	uuser = User.objects.get(username = username)
	if uuser == request.user:
		return HttpResponseRedirect('/POI/mypoints/')
	isconfirmed = False
	issent = False
	isreceived = False
	if request.user:
		friendship = Friend.objects.filter(who = request.user, fwith = uuser, confirmed = True)
		if not friendship:
			friendship = Friend.objects.filter(who = uuser, fwith = request.user, confirmed = True)
		if friendship:
			isconfirmed = True
		friendship = Friend.objects.filter(who = request.user, fwith = uuser, confirmed = False)
		if friendship:
			issent = True
		friendship = Friend.objects.filter(who = uuser, fwith = request.user, confirmed = False)
		if friendship:
			isreceived = True
			
		if issent:
			if request.method == 'POST':
				friendship = Friend.objects.get(who = request.user, fwith = uuser, confirmed = False)
				friendship.delete()
				return HttpResponseRedirect('/POI/users/'+str(uuser.username)+'/')
			else:
				template = loader.get_template('PointsOfInterest/question.html')
				context = RequestContext(request, {
					 'uuser' : uuser, 'qst' : 4,
				})
				return HttpResponse(template.render(context))
		elif isreceived:
			if request.method == 'POST':
				friendship = Friend.objects.get(who = uuser, fwith = request.user, confirmed = False)
				friendship.delete()
				return HttpResponseRedirect('/POI/users/'+str(uuser.username)+'/')
			else:
				template = loader.get_template('PointsOfInterest/question.html')
				context = RequestContext(request, {
					 'uuser' : uuser, 'qst' : 5,
				})
				return HttpResponse(template.render(context))
		elif isconfirmed:
			if request.method == 'POST':
				friendship = Friend.objects.get(who = request.user, fwith = uuser, confirmed = True)
				if friendship:
					friendship.delete()
				else:
					friendship = Friend.objects.get(who = uuser, fwith = request.user, confirmed = True)
					friendship.delete()
				return HttpResponseRedirect('/POI/users/'+str(uuser.username)+'/')
			else:
				template = loader.get_template('PointsOfInterest/question.html')
				context = RequestContext(request, {
					 'uuser' : uuser, 'qst' : 6,
				})
				return HttpResponse(template.render(context))
			return HttpResponse(template.render(context))
		elif not (isconfirmed and issent and isreceived):
			template = loader.get_template('PointsOfInterest/error.html')
			context = RequestContext(request, {
					'err': 8,
					'username': uuser.username,
				})
			return HttpResponse(template.render(context))
		else:
			template = loader.get_template('PointsOfInterest/error.html')
			context = RequestContext(request, {
					'err': 0,
				})
			return HttpResponse(template.render(context))

@login_required(login_url='/POI/login/')
def mybigmap(request):
	points = PointOfInterest.objects.filter(userid = request.user)
	template = loader.get_template('PointsOfInterest/bigmap.html')
	context = RequestContext(request, {
		'points' : points,
		})
	return HttpResponse(template.render(context))


def userbigmap(request, username):
	uuser = User.objects.get(username = username)
	if uuser == request.user:
		return HttpResponseRedirect('/POI/mypoints/bigmap')
	isconfirmed = False
	if request.user:
		friendship = Friend.objects.filter(who = request.user, fwith = uuser, confirmed = True)
		if not friendship:
			friendship = Friend.objects.filter(who = uuser, fwith = request.user, confirmed = True)
		if friendship:
			isconfirmed = True
	points1 = PointOfInterest.objects.filter(userid = uuser).filter(category = 'o')
	if isconfirmed:
		points2 = PointOfInterest.objects.filter(userid = uuser).filter(category = 'f')
		points = points1 | points2
	else:
		points = points1
	template = loader.get_template('PointsOfInterest/bigmap.html')
	context = RequestContext(request, {
		'points' : points,
		})
	return HttpResponse(template.render(context))


"""
form = CreatePoi(request.POST)
		if form.is_valid():
			place = PointOfInterest()
			place.userid = request.user

			place.title = form.cleaned_data['title']
"""


def registration(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			passagain = form.cleaned_data['passagain']
			uuser = User.objects.create_user(username, email, password)
			uuser.save()
			template = loader.get_template('PointsOfInterest/login.html')
			context = RequestContext(request, { })
			return HttpResponse(template.render(context))
		else:
			form = RegistrationForm(request.POST)
			template = loader.get_template('PointsOfInterest/registration.html')
			context = RequestContext(request, {
				'form' : form,
				})
			return HttpResponse(template.render(context))
	else:
		form = RegistrationForm()
		template = loader.get_template('PointsOfInterest/registration.html')
		context = RequestContext(request, {
			'form' : form,
			})
		return HttpResponse(template.render(context))


def find(request):
	if request.method == 'POST':
		form = FindForm(request.POST)
		if form.is_valid():
			regex = form.cleaned_data['username']
			found = User.objects.filter(username__iregex = regex)
			form = FindForm()
			template = loader.get_template('PointsOfInterest/find.html')
			context = RequestContext(request, {
				'form' : form,
				'found' : found,
			})
			return HttpResponse(template.render(context))
		else:
			form = FindForm(request.POST)
			template = loader.get_template('PointsOfInterest/find.html')
			context = RequestContext(request, {
				'form' : form,
			})
			return HttpResponse(template.render(context))
	else:
		form = FindForm()
		template = loader.get_template('PointsOfInterest/find.html')
		context = RequestContext(request, {
			'form': form,
		})
		return HttpResponse(template.render(context))
	
	
	

def delcomm(request, commid):
	comment = Commentary.objects.get(id = commid)
	if request.user == comment.userid or request.user == comment.poiid.userid:	
		if request.method == 'POST':
			comment.delete()
			return HttpResponseRedirect('/POI/place/'+str(comment.poiid.id)+'/')
		else:
			return HttpResponseRedirect('/POI/place/'+str(comment.poiid.id)+'/')
	else:
		template = loader.get_template('PointsOfInterest/error.html')
		context = RequestContext(request, {
				'err': 10,
			})
		return HttpResponse(template.render(context))



    #place = PointOfInterest.objects.get(id=placeid)
	#template = loader.get_template('POI/places.html')
    #context = RequestContext(request, { } )
    #    'place': place,
    #    })
    #return HttpResponse(template.render(context))
    #return HttpResponse("You're looking at the results of poll %s." % p.title)
	#return HttpResponse(template.render(1))
