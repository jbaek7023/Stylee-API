import random
import string

from django.utils.text import slugify
'''
random_string_generator is located here:
http://joincfe.com/blog/random-string-generator-in-python/
'''

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def create_unique_username(instance, username=None):
    # instance : Profile
    if not username:
        username = str(instance.user)

    # only allow lower case for the username
    username = username.lower()

    # User doesn't expect to
    exists = Profile.objects.filter(username=username).exists()
    if exists:
        new_username = "%s%s" % (username, random_string_generator(size=1))
        return create_unique_username(instance, username=new_username)
    return username
