import requests
import json
from django.db import models

class LiveStreams(object):
	def load(self, channel):
		r = requests.get('https://api.twitch.tv/kraken/streams/' + channel)
		json = r.json()
		if json['stream']:
			stream = Stream()
			stream.channel_name = json['stream']['channel']['display_name']
			stream.image_url = 'http://localhost:9000/images/live-stream-game.png'
			return stream
		else:
			return None

class Stream(object):
	def __init__(self):
		self.channel_name = ''
		self.image_url = ''

class StreamEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, Stream):
            return super(StreamEncoder, self).default(obj)

        return obj.__dict__