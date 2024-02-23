from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Album, Song, UserComment
from .forms import AlbumForm, SongForm

class AlbumModelTest(TestCase):
    def setUp(self):
        self.album = Album.objects.create(
            title="Test Album",
            description="Test description",
            artist="Test Artist",
            price=10,
            format="CD",
            release_date="2023-01-01",
        )

    def test_album_creation(self):
        self.assertEqual(str(self.album), "Test Album")
        self.assertEqual(self.album.get_comments().count(), 0)

class SongModelTest(TestCase):
    def setUp(self):
        self.album = Album.objects.create(
            title="Test Album",
            artist="Test Artist",
            price=10,
            format="CD",
            release_date="2023-01-01",
        )
        self.song = Song.objects.create(
            title="Test Song",
            runtime=180,
        )
        self.song.albums.add(self.album)

    def test_song_creation(self):
        self.assertEqual(str(self.song), "Test Song")
        self.assertEqual(self.song.albums.count(), 1)

class UserCommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )
        self.album = Album.objects.create(
            title="Test Album",
            artist="Test Artist",
            price=10,
            format="CD",
            release_date="2023-01-01",
        )
        self.comment = UserComment.objects.create(
            user=self.user,
            album=self.album,
            message="Test Comment"
        )

    def test_comment_creation(self):
        self.assertEqual(str(self.comment), "testuser on Test Album: Test Comment")

class AlbumFormTest(TestCase):
    def test_valid_album_form(self):
        form_data = {
            "title": "Test Album",
            "description": "Test description",
            "artist": "Test Artist",
            "price": 10,
            "format": "CD",
            "release_date": "2023-01-01",
        }
        form = AlbumForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_album_form(self):
        form_data = {
            # Incomplete data to make the form invalid
            "title": "Test Album",
            "price": 10,
        }
        form = AlbumForm(data=form_data)
        self.assertFalse(form.is_valid())

class SongFormTest(TestCase):
    def test_valid_song_form(self):
        album = Album.objects.create(title="Test Album", artist="Test Artist", price=10, format="CD", release_date="2023-01-01")
        
        form_data = {
            "title": "Test Song",
            "runtime": 180,
            "albums": [album.id],  
        }
        form = SongForm(data=form_data)

        if not form.is_valid():
            print("Validation Errors:", form.errors.as_data())

        self.assertTrue(form.is_valid())

    def test_invalid_song_form(self):
        form_data = {
            # Incomplete data to make the form invalid
            "title": "Test Song",
        }
        form = SongForm(data=form_data)
        
        if form.is_valid():
            print("Unexpectedly valid form.")

        self.assertFalse(form.is_valid())

class ViewsTest(TestCase):
    def setUp(self):
        self.album = Album.objects.create(
            title="Test Album",
            artist="Test Artist",
            price=10,
            format="CD",
            release_date="2023-01-01",
        )

    def test_album_list_view(self):
        response = self.client.get(reverse("album-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "list_view.html")

    def test_album_detail_view(self):
        response = self.client.get(reverse("album-detail", args=[self.album.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "detail_view.html")

