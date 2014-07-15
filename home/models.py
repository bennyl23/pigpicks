import datetime
from django.db import models
from tinymce.models import HTMLField

# Create your models here.
class BlogEntry(models.Model):
    entry_id = models.AutoField(primary_key=True)
    entry_date = models.DateTimeField(editable=False)
    entry_subject = models.CharField(max_length=255)
    entry_body = HTMLField()

    class Meta:
        db_table = 'blog_t'

    def __unicode__(self):
        return unicode(self.entry_subject)

    def save(self, *args, **kwargs):
        self.entry_date = datetime.datetime.now()

        super(BlogEntry, self).save(*args, **kwargs)

