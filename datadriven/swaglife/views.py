import numpy
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

def events(request):
    cost = float(request.GET.get('cost'))
    events = models.PublicEvent.objects.all()
    events_dict = {e.id: e.price for e in events.filter(price__gt=0)}
    best_variant, min_rest = get_best_bundle_events_2(events_dict, cost)
    events_output = models.PublicEvent.objects.filter(id__in=list(best_variant)).order_by('-price')
    events_list = [{'id': e.id, 'name': e.name, 'price': e.price, 'venue': e.venue} for e in events_output]
    return JsonResponse({'objects': events_list})
