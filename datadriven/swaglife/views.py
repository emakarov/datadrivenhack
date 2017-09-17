import numpy
from haversine import haversine
from django.shortcuts import render
from django.http import JsonResponse
from swaglife import models

def index(request):
    return render(request, 'swaglife/index.html', {})


def get_best_bundle_events(events_price, max_budget, search_deep=100):
   variants = []
   for i in range(search_deep):
       size = numpy.random.randint(low=1, high=len(events_price))
       variant = {}
       variant['ids'] = numpy.random.choice(list(events_price.keys()), size=size, replace=False)
       variant['sum'] = sum(events_price[id] for id in variant['ids'])
       variants.append(variant)
   min_rest = numpy.inf
   best_variant = []
   for variant in variants:
       rest = max_budget - variant['sum']
       if rest >= 0 and rest<min_rest:
           min_rest = rest
           best_variant = variant['ids']
   return best_variant, min_rest


def get_best_bundle_events_2(events_price, max_budget):
   selected_events = set()
   rest_budget = max_budget
   possible_events = {event: price for event, price in events_price.items() if price<=rest_budget and event not in selected_events}
   while len(possible_events) > 0:
       chooce_key = numpy.random.choice(list(possible_events.keys()))
       selected_events.add(chooce_key)
       rest_budget -= events_price[chooce_key]
       possible_events = {event: price for event, price in events_price.items() if price<=rest_budget and event not in selected_events}
   return selected_events, rest_budget

def is_taxi_accesible(max_price, home_lat, home_lon, office_lat, office_lon, taxi_fee=0.4, taxi_per_km=0.6, coeff=1.3):
   distance = haversine((home_lat, home_lon), (office_lat, office_lon)) * 1000 * 2
   price = coeff * distance/1000 * taxi_per_km + taxi_fee
   price = 2*price
   return price <= max_price

def events(request):
    cost = float(request.GET.get('cost'))
    events = models.PublicEvent.objects.all()
    events_dict = {e.id: e.price for e in events.filter(price__gt=0)}
    best_variant, min_rest = get_best_bundle_events_2(events_dict, cost)
    events_output = models.PublicEvent.objects.filter(id__in=list(best_variant)).order_by('-price')
    events_list = [{'id': e.id, 'name': e.name, 'price': e.price, 'venue': e.venue} for e in events_output]
    return JsonResponse({'objects': events_list})


def properties(request):
    cost = float(request.GET.get('cost'))
    transit_cost = float(request.GET.get('transit_cost'))
    transit_lat = float(request.GET.get('transit_lat'))
    transit_lon = float(request.GET.get('transit_lon'))
    flats = models.PropertyRental.objects.filter(price__lt=cost).order_by('-rating')[0:20]
    flats_list = [{'address': p.address, 'price': p.price, 'rating': p.rating, 'bedrooms': p.bedrooms, 'prop_type': p.property_type, 'img': p.image_1, 'img2': p.image_2, 'lat': p.lat, 'lon': p.lon} for p in flats]
    flats_list_with_transit = []
    for f in flats_list:
        f['taxi'] = is_taxi_accesible(transit_cost/30, transit_lat, transit_lon, f['lat'], f['lon']) 
        flats_list_with_transit.append(f)
    return JsonResponse({'objects': flats_list_with_transit})

def food(request):
    cost = float(request.GET.get('cost'))/30
    breakfast_cost = cost*0.3
    lunch_cost = cost*0.3
    dinner_cost = cost*0.6
    breakfast_foods = models.Food.objects.filter(price__lt=breakfast_cost, food_type='breafast').all()
    breakfast_foods_dict = {f.id: f.price for f in breakfast_foods}
    breakfast_possible, c = get_best_bundle_events_2(breakfast_foods_dict, breakfast_cost)
    breakfast_possible = list(breakfast_possible)
    
    lunch_foods = models.Food.objects.filter(price__lt=lunch_cost, food_type='lunch').all()
    lunch_foods_dict = {f.id: f.price for f in lunch_foods}
    lunch_possible, _ = get_best_bundle_events_2(lunch_foods_dict, lunch_cost)
    lunch_possible = list(lunch_possible)

    dinner_foods = models.Food.objects.filter(price__lt=dinner_cost, food_type='dinner').all()
    dinner_foods_dict = {f.id: f.price for f in dinner_foods}
    dinner_possible, _ = get_best_bundle_events_2(dinner_foods_dict, dinner_cost)
    dinner_possible = list(dinner_possible)

    len_break = len(breakfast_possible)
    len_lunch = len(lunch_possible)
    len_dinner = len(dinner_possible)

    foods = []
    for i in range(min(len_lunch, len_break, len_dinner)):
        breakfast_id = lunch_possible[i]
        lunch_id = breakfast_possible[i]
        dinner_id = dinner_possible[i]
        b = models.Food.objects.get(id=breakfast_id)
        lun = models.Food.objects.get(id=lunch_id)
        d = models.Food.objects.get(id=dinner_id)
        food = {'breakfast': {'price': b.price, 'name': b.name, 'venue': b.venue}, 'lunch': {'price': lun.price, 'name': lun.name, 'venue': lun.venue}, 'dinner': {'price': d.price, 'name': d.name, 'venue': d.venue}}
        foods.append(food)
    return JsonResponse({'objects': foods})

