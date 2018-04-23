from django.contrib import admin


from .models import Beer, RecentBeer, RecommendedBeer


class BeerAdmin(admin.ModelAdmin):
    exclude = ('beer_learning',)


admin.site.register(Beer, BeerAdmin)
admin.site.register(RecentBeer)
admin.site.register(RecommendedBeer)