from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.signing import Signer


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_email = models.EmailField(max_length=100)
    user_team_name = models.CharField(max_length=25)
    user_password = models.CharField(max_length=60, editable=False)
    user_paid = models.BooleanField(default=False)
    user_n = models.CharField(max_length=15, null=True, blank=True)
    user_af1 = models.CharField(max_length=15, null=True, blank=True)
    user_af2 = models.CharField(max_length=15, null=True, blank=True)
    user_fake_email = models.BooleanField(default=False)
    user_referring_email = models.EmailField(max_length=100)
    user_reset_password = models.BooleanField(default=False)

    class Meta:
        db_table = 'users_t'

    def __unicode__(self):
        return unicode(self.user_team_name + ', ' + self.user_email)

    def save(self, *args, **kwargs):
        hashed_password = make_password(self.user_password)
        self.user_password = hashed_password

        super(User, self).save(*args, **kwargs)


