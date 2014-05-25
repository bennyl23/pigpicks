from django.db import models


# Create your models here.
class Commissioner(models.Model):
    commish_id = models.PositiveSmallIntegerField(primary_key=True)
    league_message = models.TextField()
    league_rules = models.TextField()

    class Meta:
        db_table = 'commissioner_t'
