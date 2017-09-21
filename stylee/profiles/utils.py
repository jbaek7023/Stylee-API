# create  unique username
import random
import string
from django.utils.text import slugify

# from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
# User = get_user_model()

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def create_unique_username(instance, username=None):
    # instance : Profile
    if not username:
        username = str(instance.username)

    # only allow lower case for the username
    username = username.lower()

    # User doesn't expect to
    exists = User.objects.filter(username=username).exists()
    if exists:
        new_username = "%s%s" % (username, random_string_generator(size=1))
        return create_unique_username(instance, username=new_username)
    return username
