from django.shortcuts import render, redirect, get_object_or_404
from django.urls import path, reverse_lazy
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.views.generic import (
    ListView, DetailView, CreateView, DeleteView, View
)
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django import forms
from .models import Album, Song, UserComment
from .forms import AlbumForm, SongForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from datetime import datetime, date



def album_list(request):
    context = {}
    # Annotate each album with the count of associated comments
    albums_with_comments_count = Album.objects.annotate(comments_count=Count('usercomment'))

    context["album_list"] = albums_with_comments_count
    return render(request, "list_view.html", context)

def album_detail(request, pk):  #detail_view
    context={}
    context["album"] = get_object_or_404(Album , pk = pk )
    return render(request, "detail_view.html", context)

def add_existing_songs(request, album_id):
    album = Album.objects.get(pk=album_id)
    existing_songs = Song.objects.exclude(albums=album)

    if request.method == 'POST':
        selected_songs_ids = request.POST.getlist('selected_songs')
        selected_songs = Song.objects.filter(id__in=selected_songs_ids)
        album.song_set.add(*selected_songs)  

        # Redirect to the album detail page after adding songs
        return redirect('album-detail', pk=album_id)

    context = {'album': album, 'existing_songs': existing_songs}
    return render(request, 'add_existing_songs.html', context)


def album_songs(request, pk):

    album = Album.objects.get(pk=pk)
    
    songs_list = Song.objects.filter(albums=pk)

    context = {
        'album': album,
        'songs_list': songs_list
    }

    return render(request, 'song_list.html', context)
    

class add_song(CreateView):
    model = Song
    form_class = SongForm
    template_name= "create_view.html"
    def get_initial(self): 
        album = Album.objects.get(id=self.kwargs['pk'])
        return {'album': album}
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Song added successfully!')
        return response
    def get_success_url(self):
        return reverse_lazy('album-list')
    
    
def update_album(request, pk):
    context = {}
    # fetch the object related to passed id
    obj = get_object_or_404(Album, pk=pk)

    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Album Updated')
            return redirect('album-detail', pk=pk)
        else:
            messages.error(request, 'Form is not valid. Please check the data.')

    else:
        form = AlbumForm(instance=obj)

    context["form"] = form
    return render(request, "update_view.html", context)


def create_album(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            album = form.save(commit=False)

            # Check if 'cover_art' is present in request.FILES before accessing it
            if 'cover_art' in request.FILES:
                album.cover_art = request.FILES['cover_art']
                
            album.save()

            messages.success(request, 'Album created!')
            return redirect('album-detail', album.pk)
        else:
            # Form is not valid, render the form with errors
            messages.error(request, 'Error creating album. Please correct the form.')
    else:
        form = AlbumForm()

    context = {'form': form}
    return render(request, 'create_view.html', context)



def delete_album(request, pk):
    # fetch the object related to passed id
    obj = get_object_or_404(Album, pk = pk)
    # delete object
    obj.delete()
    messages.add_message(request, messages.SUCCESS, 'Album Deleted')
    # after deleting redirect to index view
    return redirect('album-list')


def remove_song_from_album(request, pk=None, song_pk=None):
    album = get_object_or_404(Album, id= pk )
    song = get_object_or_404(Song,  id =song_pk)
    song.albums.remove(album)
    messages.add_message(request, messages.INFO, ('songDeleted'))
    return HttpResponseRedirect(
        reverse_lazy('album-detail', kwargs={'pk': pk}))


def album_comments(request, pk):
    album = get_object_or_404(Album, pk=pk)
    comments = album.get_comments()
    context = {'album': album, 'comments': comments}
    return render(request, 'album_comments.html', context)


@login_required 
def account_management(request):
    user = request.user
    comments = UserComment.objects.filter(user=user)
    context = {'user': user, 'comments': comments}
    return render(request, 'account_management.html', context)


@login_required
def add_comment(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    
    if request.method == 'POST':
        message = request.POST.get('comment_message', '')
        if message:
            album.add_comment(user=request.user, message=message)
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Comment cannot be empty.')

    return redirect('album-detail', pk=album_id)


@login_required
def recommend_a_friend(request, pk):
    try:
        album = Album.objects.get(pk=pk)
    except (ObjectDoesNotExist, ValueError):
        raise Http404("Album not found.")

    template = "email_templates/recommendation_email.txt"  # Adjust the path to your email template
    return render(request, 'recommend_a_friend.html', {'album': album, 'email_template': template})


@login_required
def send_recommendation(request):
    if request.method == 'POST':
        album_id = request.POST.get('album_id')
        friend_email = request.POST.get('friend_email')
        subject = request.POST.get('email_subject')
        message = request.POST.get('email_message')

        try:
            album = Album.objects.get(pk=album_id)

            email_content = render_to_string('recommendation_email.txt', {'album': album, 'message': message})

            # Instead of sending, you can print the email content for testing purposes
            print("Recommendation Email Content:")
            print(email_content)

            # Send the email
            send_mail(
                subject="Recommendation: Check out this album!",
                message=email_content,
                from_email="your_email@example.com",  # Replace with your email
                recipient_list=[friend_email],
                fail_silently=False,
            )

            success_message = "Recommendation sent successfully."
            return render(request, 'recommend_a_friend.html', {'success_message': success_message})
        except (ObjectDoesNotExist, ValueError):
            error_message = "Error: Album not found."
            return render(request, 'recommend_a_friend.html', {'error_message': error_message})
    else:
        return HttpResponse("Invalid request method.")