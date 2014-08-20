from django.db import models

class Game(models.Model):
	image_url = models.CharField(max_length=2048)
	live_stream_image_url = models.CharField(max_length=2048)
