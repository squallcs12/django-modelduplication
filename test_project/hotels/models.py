from django.db import models


class Hotel(models.Model):
    name = models.CharField(max_length=255)
    features = models.ManyToManyField('hotels.Feature')

    def pre_duplicate(self, origin, first_level):
        if first_level:
            self.name = '{} - Duplicated'.format(self.name)

    def post_duplicate(self, origin):
        pass


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def pre_duplicate(self, origin, first_level):
        if first_level:
            self.name = '{} - Duplicated'.format(self.name)


class Feature(models.Model):
    name = models.CharField(max_length=255)


class RoomItem(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)


class HotelDistance(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)


class Booking(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    total = models.IntegerField()