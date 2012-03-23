import re

from .models import Tournament

re_tourney_matcher = re.compile(r'^/(?P<tournament>[\w_-]+)/')

def tournament(request):
    context = {'tournament_slug':re_tourney_matcher.search(request.path).group('tournament')}
    try:
        context['tournament'] = Tournament.objects.get(slug=context['tournament_slug'])
    except Tournament.DoesNotExist:
        pass
    return context
