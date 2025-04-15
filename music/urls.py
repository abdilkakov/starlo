from django.urls import path
from .views import home, upload_track, create_album, artist_dashboard, register, user_login, user_logout, albums, album_detail, all_tracks, artist_profile, edit_track, delete_track, artist_tracks, search
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", home, name="home"),
    path("upload_track/", upload_track, name="upload_track"),
    path("create_album/", create_album, name="create_album"),
    path("dashboard/", artist_dashboard, name="artist_dashboard"),
    path('register/', register, name='register'),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path('albums/', albums, name='albums'),
    path('album/<int:album_id>/', album_detail, name='album_detail'),
    path('tracks/', all_tracks, name='all_tracks'),
    path('artist/<str:username>/', artist_profile, name='artist-profile'),
    path('track/edit/<int:track_id>/', edit_track, name='edit-track'),
    path('track/delete/<int:track_id>/', delete_track, name='delete-track'),
    path('artist_tracks/', artist_tracks, name='artist_tracks'),
    path('search/', search, name='search_by_song'),
]
