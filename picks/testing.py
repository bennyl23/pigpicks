from picks.models import WinsView

wins_count = WinsView.objects.get_wins_count_by_user_week(1, 1)
print wins_count.user_id