from django.contrib import admin
from .models import Player, PointScoringEvent, Team, Game, WeekPlayerPoints, Fantasy, Season, TransferWindow, Squad, FantasySquadWeek
def delete_unused_squads(modeladmin, request, queryset):
	# Only delete squads not referenced by any Fantasy or FantasySquadWeek
	used_squad_ids = set(Fantasy.objects.exclude(currentSquad=None).values_list('currentSquad', flat=True))
	used_squad_ids |= set(FantasySquadWeek.objects.values_list('squad', flat=True))
	unused_squads = Squad.objects.exclude(id__in=used_squad_ids)
	count = unused_squads.count()
	unused_squads.delete()
	modeladmin.message_user(request, f"Deleted {count} unused squads.")

@admin.register(Squad)
class SquadAdmin(admin.ModelAdmin):
	actions = [delete_unused_squads]


# Register your models here.
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
	list_display = ("name", "team", "position", "cost", "is_active")
	list_editable = ("is_active",)
	list_filter = ("is_active", "team", "position")
	search_fields = ("name",)

admin.site.register(Team)
admin.site.register(Game)
admin.site.register(PointScoringEvent)
admin.site.register(WeekPlayerPoints)
admin.site.register(Fantasy)
admin.site.register(Season)
admin.site.register(TransferWindow)
