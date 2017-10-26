from django.contrib import admin
from .models import Movie
from django.core import management
from django.shortcuts import redirect

class MovieAdmin(admin.ModelAdmin):
    @admin.site.register_view('import_movies_from_url', 'Import Movies from URL')
    def import_movies_from_url(request):
        print('import movies here')
        try:
            management.call_command('import_from_url')
            message = 'successfully imported data from URL'

        except Exception as ex:
            message = 'Error importing from data from URL {}'.format(str(ex))

        admin.ModelAdmin.message_user(Movie, request, message)
        return redirect('admin:index')

admin.site.register(Movie, MovieAdmin)

