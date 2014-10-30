from django.db import models

from .fields import ColourField
from .managers import GameManager, CarouselItemManager

from profiles.fields import HTMLField


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

    questions = HTMLField(tags=['ol', 'ul', 'li', 'strong', 'em', 'p'], blank=True, default="""<ol><li>
<p>Why did you choose this race/champion?</p>
<p>-</p>
</li>
<li>
<p>What do you do for a living?  What do you love about your job?</p>
<p>-</p>
</li>
<li>
<p>What other hobbies do you have?</p>
<p>-</p>
</li>
<li>
<p>Why do you play StarCraft/League of Legends?</p>
<p>-</p>
</li>
<li>
<p>How long have you been playing?</p>
<p>-</p>
</li>
<li>
<p>What have you done to prepare for the momentous challenge that is the AHGL Tournament?</p>
<p>-</p>
</li>
<li>
<p>Why is your team going to win?</p>
<p>-</p>
</li>
<li>
<p>Who is the best player on your team?  Why?</p>
<p>-</p>
</li>
<li>
<p>Whom do you fear most amongst the competition and why?</p>
<p>-</p>
</li>
</ol>""")

    objects = GameManager()


    def __unicode__(self):
        return self.name

    def get_tournament_slug(self, *args, **kwargs):
        if self.tournament is None:
            return ""

        return self.tournament.slug

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

    objects = CarouselItemManager()

    def __unicode__(self):
        return self.image_url
