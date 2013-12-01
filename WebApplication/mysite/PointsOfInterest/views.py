from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader


from PointsOfInterest.models import PointOfInterest

def index(request):
    return HttpResponse("Hello, world. You're at our exciting site about Points of Interest")

def place(request, placeid):
    place = PointOfInterest.objects.get(id=placeid)
    template = loader.get_template('PointsOfInterest/place.html')
    context = RequestContext(request, {
        'place': place,
        })
    return HttpResponse(template.render(context))
    #return HttpResponse("You're looking at the results of poll %s." % p.title)

def places(request, userid):
	places = PointOfInterest.objects.filter(user_id=userid)
	template = loader.get_template('PointsOfInterest/places.html')
	context = RequestContext(request, {
        'places': places,
        })
	return HttpResponse(template.render(context))
    #place = PointOfInterest.objects.get(id=placeid)
	#template = loader.get_template('PointsOfInterest/places.html')
    #context = RequestContext(request, { } )
    #    'place': place,
    #    })
    #return HttpResponse(template.render(context))
    #return HttpResponse("You're looking at the results of poll %s." % p.title)
	#return HttpResponse(template.render(1))
