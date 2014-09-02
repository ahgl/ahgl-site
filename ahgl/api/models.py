from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.CharField(max_length=2048)
    live_stream_image_url = models.CharField(max_length=2048)
    channel_name = models.CharField(max_length=100)
    tournament = models.ForeignKey('tournaments.Tournament')

    def __unicode__(self):
        return self.name


class CarouselItem(models.Model):
    order = models.IntegerField()
    message = models.CharField(max_length=2048)
    image_url = models.CharField(max_length=2048)

    def __unicode__(self):
        return self.image_url
