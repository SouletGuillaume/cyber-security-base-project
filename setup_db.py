import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import UserBank

User.objects.all().delete() # delete all existing users

admin = User.objects.create_superuser('admin', '', 'admin123') # simulate an admin user

# list of users to create
users = [
    ('alice', 'redqueen'),
    ('bob', 'spongebob')
]

# create users and their bank accounts
for username, password in users:
    User.objects.create_user(username=username, password=password)
