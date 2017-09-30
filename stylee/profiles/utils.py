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
    print('---------------------')
    print('1start')
    print(username)
    if not username:
        username = str(instance.username)

    print('---------------------')
    print('2AssignUsername if it is not')
    print(username)
    # only allow lower case for the username
    username = username.lower()

    # User doesn't expect to
    exists = User.objects.filter(username=username).exists()
    # alreayd created.
    print('---------------------')
    print('3Check if it has a matching username')
    print(User.objects.filter(username=username))
    print(exists)
    if exists:
        print('---------------------')
        print('3.5 in the exists if statement')
        new_username = "%s%s" % (username, random_string_generator(size=1))
        return create_unique_username(instance, username=new_username)
    print('---------------------')
    print('Right Before The End')
    print(username)
    print('end')
    return username
