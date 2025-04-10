from django.contrib import admin
from .models import Artist, Track, Album, Listener
class TrackInline(admin.TabularInline):
    model = Album.tracks.through
    extra = 1

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Listener)
class ListenerAdmin(admin.ModelAdmin):
    list_display = ("user",)
@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ("title", "artist")
    search_fields = ("title",)

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("title", "artist", "release_date")
    search_fields = ("title",)
    inlines = [TrackInline]
