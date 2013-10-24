from django.contrib.auth.models import UserManager, AbstractUser

# extend Django's built-in AbstractUser with a few properties
class UserProfile(AbstractUser):
    class Meta:
        db_table = 'testsuite_app_userprofile'
        app_label= 'testsuite_app'

    objects = UserManager()
