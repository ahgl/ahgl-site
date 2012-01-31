# Create your views here.
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from models import Team

class TeamDetailView(DetailView):
    def get_queryset(self):
        return Team.objects.filter(tournament=self.kwargs['tournament'])
    
class TeamListView(ListView):
    def get_queryset(self):
        return Team.objects.filter(tournament=self.kwargs['tournament']).order_by('name')
    
class StandingsView(ListView):
    def get_queryset(self):
        return Team.objects.filter(tournament=self.kwargs['tournament']).order_by('rank')

    def get_template_names(self):
        return "profiles/standings.html"