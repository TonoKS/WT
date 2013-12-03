from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import auth


from django.contrib.auth.models import User


from PointsOfInterest.models import PointOfInterest
from PointsOfInterest.models import CreatePoi
from PointsOfInterest.models import Login


def index(request):
	return HttpResponse("Hello, world. You're at our exciting site about Points of Interest")

def loggingout(request):
	auth.logout(request)
	template = loader.get_template('PointsOfInterest/login.html')
	context = RequestContext(request, {	})
	return HttpResponse(template.render(context))


def logging(request):
	#request.session['test'] = 'test'
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				request.session['logged'] = user.id
				# Redirect to a success page.
				template = loader.get_template('PointsOfInterest/login.html')
				context = RequestContext(request, { 'logged' : True })
				return HttpResponse(template.render(context))
			else:
				# Return a 'disabled account' error message
				return HttpResponse("Ucet neaktivny")
		else:
			# Return an 'invalid login' error message.
			# return HttpResponse("Neprihlaseny")
			template = loader.get_template('PointsOfInterest/login.html')
			context = RequestContext(request, { 'message' :"Nespravne prihlasovacie udaje", 'logged' : False,	})
			return HttpResponse(template.render(context))
	elif 'logged' in request.session:
		template = loader.get_template('PointsOfInterest/login.html')
		context = RequestContext(request, { 'message' :"Uz ste prihlaseny", 'logged' : True,	})
		return HttpResponse(template.render(context))
	else:
		template = loader.get_template('PointsOfInterest/login.html')
		context = RequestContext(request, { 'logged' : False, })
		return HttpResponse(template.render(context))



def place(request, placeid):
	place = PointOfInterest.objects.get(id=placeid)
	template = loader.get_template('PointsOfInterest/place.html')
	context = RequestContext(request, {
		'place': place,
		})
	return HttpResponse(template.render(context))

@login_required(login_url='/POI/login/')
def places(request):
	userid = request.session['logged']
	places = PointOfInterest.objects.filter(user_id=userid)
	template = loader.get_template('PointsOfInterest/places.html')
	context = RequestContext(request, {
        'places': places,
        })
	return HttpResponse(template.render(context))



def createpoi(request):
	if request.method == 'POST': # If the form has been submitted...
		form = CreatePoi(request.POST) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			# Process the data in form.cleaned_data
			# ...

			place = PointOfInterest()
			place.title = form.cleaned_data['title']
			place.description = form.cleaned_data['description']
			place.latitude = form.cleaned_data['latitude']
			place.longitude = form.cleaned_data['longitude']
			place.user_id = 1
			place.category_id = 1
			place.photos_id = 1

			place.save()

			template = loader.get_template('PointsOfInterest/index.html')
			context = RequestContext(request, {
		})
		return HttpResponse(template.render(context))
			#return HttpResponse('/POI/index.html')
	else:
		form = CreatePoi() # An unbound form
		template = loader.get_template('PointsOfInterest/createpoi.html')
		"""return render(request, 'PointsOfInterest/createpoi.html', {
			'form': form
		})"""
		context = RequestContext(request, {
			'form': form,
		})
		return HttpResponse(template.render(context))



def friends(request):
	return HttpResponse("Stranka priatelia")

def settings(request):
	return HttpResponse("Stranka nastavenia")




    #place = PointOfInterest.objects.get(id=placeid)
	#template = loader.get_template('PointsOfInterest/places.html')
    #context = RequestContext(request, { } )
    #    'place': place,
    #    })
    #return HttpResponse(template.render(context))
    #return HttpResponse("You're looking at the results of poll %s." % p.title)
	#return HttpResponse(template.render(1))
