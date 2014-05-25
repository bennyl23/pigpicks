from login import models


user = models.User.objects.filter(user_email='bennyl23@yahoo.com')
print(user[0])

