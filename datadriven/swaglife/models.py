from django.db import models

PROPERTY_TYPES_CHOICES = (('1', 'Condo'), ('2', 'HDB')) 
FOOD_TYPES_CHOICES = (('1', 'Breakfast'), ('2', 'Lunch'), ('3', 'Dinner'))

class PublicEvent(models.Model):
    #event_id,event_name,show_id,show_start,show_end,ticketed,base_price
    venue = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0)

    def __str__(self):
        return '{} at {}'.format(self.name, self.venue)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'


class PropertyRental(models.Model):
    address = models.CharField(default='', max_length=255)
    bedrooms = models.IntegerField()
    price = models.FloatField()
    bathrooms = models.IntegerField()
    area = models.FloatField()
    rating = models.FloatField()
    property_type = models.CharField(max_length=1, choices=PROPERTY_TYPES_CHOICES)
    property_name = models.CharField(default='', max_length=255)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    image_1 = models.CharField(default='', max_length=255)
    image_2 = models.CharField(default='', max_length=255)
    image_3 = models.CharField(default='', max_length=255)
    image_4 = models.CharField(default='', max_length=255)
    image_5 = models.CharField(default='', max_length=255)


    def __str__(self):
        return '{}b at {}'.formt(self.bedrooms, self.address) 

    class Meta:
        verbose_name = 'Property Rental'
        verbose_name_plural = 'Property Rentals'


class Food(models.Model):
    name = models.CharField(default='', max_length=255)
    price = models.FloatField()
    venue = models.CharField(default='', max_length=50)
    food_type = models.CharField(max_length=1, choices=FOOD_TYPES_CHOICES)

    def __str__(self):
        return {}.format(self.name)

    class Meta:
        verbose_name = 'Food'
