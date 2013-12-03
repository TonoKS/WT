from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader


from PointsOfInterest.models import PointOfInterest
from PointsOfInterest.models import CreatePoi


def index(request):
    return HttpResponse("Hello, world. You're at our exciting site about Points of Interest")

def place(request, placeid):
    place = PointOfInterest.objects.get(id=placeid)
    template = loader.get_template('PointsOfInterest/place.html')
    context = RequestContext(request, {
        'place': place,
        })
    return HttpResponse(template.render(context))

def places(request, userid):
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
