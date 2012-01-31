from .models import Tournament

def tournaments(request):
    return {
        'tournaments': Tournament.objects.filter(active=True)
    }
