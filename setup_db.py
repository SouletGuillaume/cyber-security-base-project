import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import UserBank

User.objects.all().delete() # delete all existing users

admin = User.objects.create_superuser('admin', '', 'admin123') # simulate an admin user
UserBank.objects.create(user=admin, balance=50000)

# list of users to create (username, password, balance)
users = [
    ('alice', 'redqueen', 100),
    ('bob', 'spongebob', 250)
]

for username, password, balance in users:
    new_user = User.objects.create_user(username=username, password=password)   
    UserBank.objects.create(user=new_user, balance=balance)

