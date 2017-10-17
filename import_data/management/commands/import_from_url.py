"""
Import json data from URL to Datababse
"""
import requests
import json
from import_data.models import Movie
from django.core.management.base import BaseCommand
from datetime import datetime

IMPORT_URL = 'https://jsonplaceholder.typicode.com/photos'


class Command(BaseCommand):
    def import_movie(self, data):
        title = data.get('title', None)
        url = data.get('url', None)
        release_year = datetime.now()

        try:
            movie, created = Movie.objects.get_or_create(
                title=title,
                url=url,
                release_year=release_year
            )
            if created:
                movie.save()
                display_format = "\nMovie, {}, has been saved."
                print(display_format.format(movie))
        except Exception as ex:
            print(str(ex))
            msg = "\n\nSomething went wrong saving this movie: {}\n{}".format(title, str(ex))
            print(msg)


    def handle(self, *args, **options):
        """
        Makes a GET request to the  API.
        """
        headers = {'Content-Type': 'application/json'}
        response = requests.get(
            url=IMPORT_URL,
            headers=headers,
        )

        response.raise_for_status()
        data = response.json()

        for data_object in data:
            self.import_movie(data_object)
