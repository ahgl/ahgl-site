from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=100)

    header_image_url = models.CharField(max_length=2048)
    section_image_url = models.CharField(max_length=2048)
    background_match_image_url = models.CharField(max_length=2048)
    icon_image_url = models.CharField(max_length=2048)

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
