from django.contrib import admin


from .models import Beer, RecentBeer

admin.site.register(Beer)
admin.site.register(RecentBeer)
