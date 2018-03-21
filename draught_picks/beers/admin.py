from django.contrib import admin


from .models import Beer, RecentBeer, RecommendedBeer

admin.site.register(Beer)
admin.site.register(RecentBeer)
admin.site.register(RecommendedBeer)