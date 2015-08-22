from django.contrib.auth.models import UserManager, AbstractUser

# extend Django's built-in AbstractUser with a few properties
class UserProfile(AbstractUser):
    objects = UserManager()
