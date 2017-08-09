from django.db.models import (
    OneToOneField,
    TextField,
    Model
)

from django.contrib.auth.models import User

# Create your models here.
class Profile(Model):
    user    =   OneToOneField(User)
    bio     =   TextField(max_length=255, blank=True)

    def __str__(self):
        return self.user
