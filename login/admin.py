from django.contrib import admin
from django.db import models
from login.models import User
from django.forms import TextInput
from login.models import Email


class UserAdmin(admin.ModelAdmin):
    fields = ['user_email', 'user_team_name', 'user_paid', 'user_paid_ben', 'user_paid_ron', 'user_n', 'user_af1', 'user_af2', 'user_referring_email']
    list_display = ['user_email', 'user_team_name', 'user_n', 'user_af1', 'user_af2', 'user_paid', 'user_paid_ben', 'user_paid_ron']
    search_fields = ['user_email', 'user_team_name', 'user_n', 'user_af1', 'user_af2']
    list_filter = ['user_paid', 'user_paid_ben', 'user_paid_ron']
    list_editable = ['user_n', 'user_af1', 'user_af2', 'user_paid', 'user_paid_ben', 'user_paid_ron']
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'10'})}
    }
    list_per_page = 1000


class EmailAdmin(admin.ModelAdmin):
    fields = ['email_subject', 'email_body']


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Email, EmailAdmin)
