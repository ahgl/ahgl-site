import re

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _

from .models import Tournament, GamePluginModel, TournamentPluginModel, Game

r_tourney_slug = re.compile('^(?P<slug>[\w_-]+)/')

def tourney_from_slug(request):
    if not hasattr(request, 'tournament'):
        slug = r_tourney_slug.match(request.path).group('slug')
        request.tournament = Tournament.objects.get(slug=slug).select_related('featured_game__map', 'featured_game__home_player', 'featured_game__away_player')
    return request.tournament

class GamePlugin(CMSPluginBase):
    model = GamePluginModel
    name = _("Game Plugin")
    render_template = "tournaments/game_plugin.html"

    def get_form(self, request, obj=None, **kwargs):
        self.obj = obj
        return super(GamePlugin, self).get_form(request, obj, **kwargs)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "game":
            kwargs["queryset"] = Game.objects.filter(match__published=True, winner_team__isnull=False, match__tournament=getattr(self.obj, 'tournament', None)) \
                                             .order_by('-match__publish_date') \
                                             .select_related('home_player', 'away_player', 'map') \
                                             .only('home_player__char_name', 'away_player__char_name', 'map__name')
        return super(GamePlugin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def render(self, context, instance, placeholder):
        context['game'] = instance.game
        if instance.game:
            context['match'] = instance.game.match
        return context
plugin_pool.register_plugin(GamePlugin)

class RandomTeamsPlugin(CMSPluginBase):
    model = TournamentPluginModel
    name = _("Random Teams Plugin")
    render_template = "tournaments/random_teams_plugin.html"

    def render(self, context, instance, placeholder):
        context['tournament'] = instance.tournament
        return context
plugin_pool.register_plugin(RandomTeamsPlugin)

class TournamentNavPlugin(CMSPluginBase):
    model = TournamentPluginModel
    name = _("Tournament Navigation")
    render_template = "tournaments/_tournament_nav.html"

    def render(self, context, instance, placeholder):
        context['tournament_slug'] = instance.tournament_id
        context['extra_header_id'] = "-ahgl2"
        return context
plugin_pool.register_plugin(TournamentNavPlugin)
