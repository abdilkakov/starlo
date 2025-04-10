from django import forms
from django.contrib.auth.models import User
from .models import Artist, Track, Album, Listener

class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ['title', 'audio_file', 'cover_image']

class AlbumForm(forms.ModelForm):
    tracks = forms.ModelMultipleChoiceField(
        queryset=Track.objects.none(),  # Позже заменим
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Album
        fields = ['title', 'cover', 'release_date', 'tracks']

    def __init__(self, *args, **kwargs):
        artist = kwargs.pop('artist', None)
        super().__init__(*args, **kwargs)
        if artist:
            self.fields['tracks'].queryset = Track.objects.filter(artist=artist)


class UserRegistrationForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('listener', 'Listener'),
        ('artist', 'Artist')
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}))
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
        label="Confirm password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            role = self.cleaned_data["role"]
            if role == "listener":
                Listener.objects.create(user=user)
            elif role == "artist":
                Artist.objects.create(user=user, name=user.username)
        return user
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match!")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        return user
class ListenerForm(forms.ModelForm):
    class Meta:
        model = Listener
        fields = ['profile_picture']
class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'image', 'bio']


class TrackUploadForm(forms.ModelForm):
    album = forms.ModelMultipleChoiceField(
        queryset=Album.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Track
        fields = ['title', 'genre', 'audio_file', 'album']