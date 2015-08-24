from django.db import models
from django.contrib.auth.hashers import make_password
from tinymce.models import HTMLField
import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.utils.html import strip_tags
from django.db.models import Q


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_email = models.EmailField(max_length=100)
    user_team_name = models.CharField(max_length=25)
    user_password = models.CharField(max_length=128, editable=False)
    user_paid = models.BooleanField(default=False)
    user_n = models.CharField(max_length=15, null=True, blank=True)
    user_af1 = models.CharField(max_length=15, null=True, blank=True)
    user_af2 = models.CharField(max_length=15, null=True, blank=True)
    user_referring_email = models.EmailField(max_length=100, blank=True)
    user_reset_password = models.BooleanField(default=False)
    user_paid_ben = models.BooleanField(default=False)
    user_paid_ron = models.BooleanField(default=False)

    class Meta:
        db_table = 'users_t'

    def __unicode__(self):
        return unicode(self.user_team_name + ', ' + self.user_email)

    def hash_password(self):
        return make_password(self.user_password)


class Email(models.Model):
    email_id = models.AutoField(primary_key=True)
    email_date = models.DateTimeField(editable=False)
    email_subject = models.CharField(max_length=255)
    email_body = HTMLField()

    class Meta:
        db_table = 'email_t'

    def __unicode__(self):
        return unicode(self.email_subject)

    def save(self, *args, **kwargs):
        self.email_date = datetime.datetime.now()

        super(Email, self).save(*args, **kwargs)

        # set email parameters and send
        from_email = 'Pig Picks Five<ben@pigpicksfive.com>'
        to_email = 'emails@pigpicksfive.com'
        bcc_user_emails = User.objects.all().values_list('user_email', flat=True)
        text_content = strip_tags(self.email_body)

        email_msg = EmailMultiAlternatives(self.email_subject, text_content, from_email, [to_email], bcc_user_emails)
        email_msg.attach_alternative(self.email_body, "text/html")
        email_msg.send()