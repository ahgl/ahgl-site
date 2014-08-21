from django.db import models

class Game(models.Model):
	name = models.CharField(max_length=100)
	image_url = models.CharField(max_length=2048)
	live_stream_image_url = models.CharField(max_length=2048)

	def __unicode__(self):
		return self.name
