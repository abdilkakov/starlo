from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Track, Album, Artist
from .forms import AlbumForm, UserRegistrationForm, ArtistForm, TrackUploadForm


def home(request):
    albums = Album.objects.all()
    return render(request, "music/home.html", {"albums": albums})

def albums(request):
    all_albums = Album.objects.all()
    return render(request, "music/albums.html", {"albums": all_albums})
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import Artist
from .forms import UserRegistrationForm, ArtistForm

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        role = request.POST.get('role')
        artist_form = ArtistForm(request.POST, request.FILES) if role == 'artist' else None

        if user_form.is_valid() and (artist_form is None or artist_form.is_valid()):
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            if role == 'artist':
                artist = artist_form.save(commit=False)
                artist.user = user
                artist.save()
                login(request, user)
                return redirect('artist_dashboard')

            login(request, user)
            return redirect('home')


    else:
        user_form = UserRegistrationForm()
        artist_form = ArtistForm()

    return render(request, 'music/register.html', {
        'user_form': user_form,
        'artist_form': artist_form
    })



def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Неправильный логин или пароль!")

    return render(request, "music/login.html")


@login_required
def user_logout(request):
    logout(request)
    return redirect("home")


@login_required
def upload_track(request):
    if not hasattr(request.user, 'artist'):
        return redirect('home')

    if request.method == 'POST':
        form = TrackUploadForm(request.POST, request.FILES)
        if form.is_valid():
            track = form.save(commit=False)
            track.artist = request.user.artist
            track.save()

            # Добавляем трек в выбранные альбомы
            albums = form.cleaned_data.get('album')
            if albums:
                for album in albums:
                    album.tracks.add(track)

            return redirect('artist_dashboard')
    else:
        form = TrackUploadForm()

    return render(request, 'music/upload_track.html', {'form': form})


@login_required
def create_album(request):
    if not hasattr(request.user, 'artist'):
        return redirect('home')

    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES, artist=request.user.artist)
        if form.is_valid():
            album = form.save(commit=False)
            album.artist = request.user.artist
            album.save()
            form.save_m2m()
            return redirect('artist_dashboard')
    else:
        form = AlbumForm(artist=request.user.artist)

    return render(request, 'music/create_album.html', {'form': form})

@login_required
def artist_dashboard(request):
    if not hasattr(request.user, 'artist'):
        return redirect('home')

    artist = request.user.artist
    albums = artist.album_set.all()
    tracks = artist.tracks.all()

    return render(request, 'music/artist_dashboard.html', {
        'artist': artist,
        'albums': albums,
        'tracks': tracks
    })

def album_detail(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    tracks = album.tracks.all()

    return render(request, 'music/album_detail.html', {
        'album': album,
        'tracks': tracks
    })
