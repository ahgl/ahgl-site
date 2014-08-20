from ahgl.api.domain import streams
#
from rest_framework.views import APIView
# from ahgl.api.serializers import streams
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

class StreamsAPIView(APIView):

    def get(self, request, format=None):
        liveStream = streams.LiveStreams()
        return Response(liveStream.load('dota 2'))
