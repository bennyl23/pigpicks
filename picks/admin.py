from django.contrib import admin

from picks.models import Week
from picks.models import NFLTeam
from picks.models import Matchup
from picks.models import Pick


class WeekAdmin(admin.ModelAdmin):
    list_display = ['week_number', 'week_start', 'week_end', 'picks_lock', 'lines_entered']
    list_editable = ['lines_entered']


class NFLTeamAdmin(admin.ModelAdmin):
    list_display = ['nfl_team_name', 'nfl_team_location']


class MatchupAdmin(admin.ModelAdmin):
    list_display = ['matchup_desc', 'game_date', 'spread', 'home_team_id', 'home_team_score', 'away_team_id', 'away_team_score', 'matchup_completed']
    list_filter = ['week_number']
    list_editable = ['home_team_score', 'away_team_score', 'matchup_completed']


class PickAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'matchup_id', 'nfl_team_id', 'won_pick']
    search_fields = ['user_id__user_email', 'user_id__user_team_name']
    list_filter = ['matchup_id__week_number']


# Register your models here.
admin.site.register(Week, WeekAdmin)
admin.site.register(NFLTeam, NFLTeamAdmin)
admin.site.register(Matchup, MatchupAdmin)
admin.site.register(Pick, PickAdmin)
