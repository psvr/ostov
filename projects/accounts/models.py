from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class User(AbstractUser):

    def __str__(self):
        return u' <{username}> {last_name}'.format(
            username=self.username,
            last_name=self.last_name,
        )
