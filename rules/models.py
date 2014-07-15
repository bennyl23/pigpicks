from django.db import models
from tinymce.models import HTMLField

# Create your models here.
class Rule(models.Model):
    rule_id = models.AutoField(primary_key=True)
    rule_text = HTMLField()

    class Meta:
        db_table = 'rules_t'

    def __unicode__(self):
        return unicode('Pig Picks Rules')