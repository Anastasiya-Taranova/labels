from django.db import models


class AuthModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.TextField()

    def __str__(self):
        return self.name
