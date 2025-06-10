# partners/context_processors.py
from .models import Partner  # ensure this import points to your model

def partners_list(request):
    # Fetch active partners (or adjust your filter logic)
    queryset = Partner.objects.all()
    return {
        'partners': queryset
    }
