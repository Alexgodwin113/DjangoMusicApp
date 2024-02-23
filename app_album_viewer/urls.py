from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.album_list , name='album-list'),
    path('<int:pk>/', views.album_detail , name='album-detail'),
    path('<int:pk>/edit', views.update_album , name='album-update'),
    path('<int:pk>/deletealbum', views.delete_album , name='album-delete'),
    path('<int:pk>/songs', views.album_songs , name='songs_list'),
    path('create/', views.create_album , name='album-create'),
    path('<int:pk>/songs/new', views.add_song.as_view() , name='add-song'),
    path('<int:pk>/songs/<int:song_pk>/deletesong', views.remove_song_from_album , name='song_delete'),
    path('<int:pk>/comments', views.album_comments, name='album-comments'),
    path('account/', views.account_management, name='account-management'),
    path('<int:album_id>/add-comment', views.add_comment, name='add-comment'),
    path('<int:album_id>/add-existing-songs/', views.add_existing_songs, name='add-existing-songs'),
    path('albums/<int:pk>/recommend-a-friend/', views.recommend_a_friend, name='recommend-a-friend'),
    path('send-recommendation/', views.send_recommendation, name='send-recommendation'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)