from django.db import models
from django.contrib.auth.hashers import make_password

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

class Offering(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offering = models.ForeignKey(Offering, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
