from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    A custom user model is highly recommended by Django, as migrating to one later
    in the project is challenging. For more information see:
    https://docs.djangoproject.com/en/3.2/topics/auth/customizing/
    """
    pass
