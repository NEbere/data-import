from django.db import models

# Movies model for data import
class Movie(models.Model):
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    release_year = models.CharField(max_length=20)