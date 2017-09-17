from swaglife.models import PublicEvent
from csv import reader

def read_csv_lines(filename):
    lines = []
    f = open(filename)
    for line in reader(f):
        lines.append(line)
    return lines

# import events:
PublicEvent.objects.all().delete()
events = read_csv_lines('esplanade_events.csv')
for event in events[1:]:
    venue = 'Esplanade'
    name = event[1]
    price = event[6]
    if price == 'NULL':
        price = 0
    else:
        price = float(price)
    ev = PublicEvent()
    ev.venue = venue
    ev.name = name
    ev.price = price
    ev.save()
    

