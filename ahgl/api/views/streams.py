from ahgl.api.domain.streams import LiveStreams, Stream, StreamEncoder
from tournaments.models import Tournament
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
import json

class StreamsAPIView(APIView):

    def get(self, request, format=None):
        liveStream = LiveStreams()

        for tournament in Tournament.objects.all():
            stream = liveStream.load(tournament.channel_name, tournament.game.live_stream_image_url)
            if stream:
                return Response(json.loads(json.dumps(stream, cls=StreamEncoder)))
                
        return Response('no streams')
