import requests
from django.db import models

class LiveStreams(object):
	_meta = models.Model
	def __init__(self):
		self.streams = []

	def load(self, game):
		payload = { 'q': game }
		r = requests.get('https://api.twitch.tv/kraken/search/streams', params=payload)
		return r.json()

