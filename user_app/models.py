# from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
        class User : inherit of AbstractUser --> no need to add  something for the moment
    """

    def __str__(self):
        return self.username
