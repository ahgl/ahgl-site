from ahgl.api.domain.streams import LiveStreams, Stream, StreamEncoder
from tournaments.models import TournamentRound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
import json

class StreamsAPIView(APIView):

    def get(self, request, format=None):
        liveStream = LiveStreams()

        for tournamentRound in TournamentRound.objects.all():
            stream = liveStream.load('GSL')
            if stream:
                return Response(json.loads(json.dumps(stream, cls=StreamEncoder)))
                
        return Response('no streams')
