from django.core.management.base import BaseCommand
from django.core.files.images import ImageFile
import json
from datetime import date
from ...models import Album,Song , UserComment
from django.contrib.auth.models import User
from pathlib import Path


ROOT_DIR = Path('app_album_viewer') / 'management' / 'commands'


class Command(BaseCommand):
    def handle(self, *args, **options):
        Album.objects.all().delete()
        Song.objects.all().delete()
        UserComment.objects.all().delete()

        with open(ROOT_DIR / 'sample_data.json') as json_file:
            sample_data = json.load(json_file)

        for album_data in sample_data['albums']:
            a = Album(
                cover_art=album_data['cover'],
                title=album_data['title'],
                description=album_data['description'],
                artist=album_data['artist'],
                price=album_data['price'],
                format=album_data['format'],
                release_date=album_data['release_date']
            )

            image_path = album_data['cover']

            if image_path is not None:
                a.cover_art = ImageFile(open(Path(ROOT_DIR / 'sample_data') / image_path, 'rb'))
            a.save()

            for comment_data in album_data.get('comments', []):
                user_display_name = comment_data.get('user__display_name', '')
                message = comment_data.get('message', '')
                user_email = comment_data.get('user__email', '')  # Extract user email
                user, _ = User.objects.get_or_create(username=user_display_name, defaults={'email': user_email})
                UserComment.objects.create(user=user, album=a, message=message)
                

                        
        for song in sample_data['songs']:
            s = Song(title = song['title'], runtime = song['runtime'])
            s.save()
            
            for album in song['albums']:
                s.albums.add(Album.objects.filter(title = album).first())
            
            s.save()
                
                
        print('Seeding Done.')