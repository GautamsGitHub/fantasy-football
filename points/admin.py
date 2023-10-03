from django.contrib import admin
from .models import Player, PointScoringEvent, Team, Game, WeekPlayerPoints, Fantasy, Season

# Register your models here.

admin.site.register(Player)
admin.site.register(Team)
admin.site.register(Game)
admin.site.register(PointScoringEvent)
admin.site.register(WeekPlayerPoints)
admin.site.register(Fantasy)
admin.site.register(Season)
