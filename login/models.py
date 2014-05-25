from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.signing import Signer


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_email = models.EmailField(max_length=100)
    user_team_name = models.CharField(max_length=25)
    user_password = models.CharField(max_length=60, editable=False)
    user_admin_access = models.BooleanField(default=False)
    user_paid = models.BooleanField(default=False)
    user_n = models.CharField(max_length=15, null=True, blank=True)
    user_af1 = models.CharField(max_length=15, null=True, blank=True)
    user_af2 = models.CharField(max_length=15, null=True, blank=True)
    user_fake_email = models.BooleanField(default=False)
    user_referring_email = models.EmailField(max_length=100)

    class Meta:
        db_table = 'users_t'

    def __unicode__(self):
        return unicode(self.user_team_name + ', ' + self.user_email)

    def create_forgot_password_link(self):
        user_id, token = self.make_token().split(":", 1)
        return 'http://www.pigpicksfive.com/login/reset_password?token=' + token

    def make_token(self):
        return Signer().sign(str(self.user_id))

    def save(self, *args, **kwargs):
        # if this is a new user
        if self.user_id is None or 'new_password' in kwargs:
            hashed_password = make_password(self.user_password)
            self.user_password = hashed_password

        super(User, self).save(*args, **kwargs)


