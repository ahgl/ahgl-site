from django.db import models

from .fields import ColourField


class Game(models.Model):
    name = models.CharField(max_length=100)

    header_image_url = models.CharField(max_length=2048)
    
    live_stream_section_image_url = models.CharField(max_length=2048)
    match_section_image_url = models.CharField(max_length=2048)
    article_section_image_url = models.CharField(max_length=2048)
    
    background_match_image_url = models.CharField(max_length=2048)
    icon_image_url = models.CharField(max_length=2048)

    small_game_thumbnail = models.CharField(max_length=2048)

    header_image_glow_hex_color = ColourField()


    def __unicode__(self):
        return self.name

    def get_tournament_slug(self, *args, **kwargs):
        tournaments = self.tournament_set.all()
        if tournaments.count() < 1:
            return ""
        return tournaments[0].slug

    @property
    def channel_name(self):
        channels = self.channel_names.filter(primary=True)

        if channels.count() < 1:
            return ""

        return channels[0].name
        

class Channel(models.Model):
    name = models.CharField(max_length=100)
    primary = models.BooleanField(default=False)
    game = models.ForeignKey('Game', related_name='channel_names')


class CarouselItem(models.Model):
    order = models.IntegerField()
    message = models.CharField(max_length=2048)
    image_url = models.CharField(max_length=2048)

    tournaments = models.ManyToManyField('tournaments.Tournament', related_name='carousel_items')

    def __unicode__(self):
        return self.image_url
