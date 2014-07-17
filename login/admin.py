from django.contrib import admin
from login.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'user_team_name', 'user_n', 'user_af1', 'user_af2', 'user_paid']
    search_fields = ['user_email', 'user_team_name', 'user_n', 'user_af1', 'user_af2']
    list_filter = ['user_paid']
    list_editable = ['user_paid']


# Register your models here.
admin.site.register(User, UserAdmin)
