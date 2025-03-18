from django.urls import path
from .views import home, upload_track, create_album, artist_dashboard, register, user_login, user_logout, albums, album_detail  # Добавьте artist_dashboard
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
]
