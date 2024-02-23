from django import forms
from .models import Album, Song
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# creating a form
class AlbumForm(forms.ModelForm):
# create meta class
    class Meta:
    # specify model to be used
        model = Album
        fields = ['title', 'description', 'artist', 'price', 
                  'format', 'release_date', 'cover_art']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'formfield',
                'placeholder': 'Album Title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'formfield',
                'placeholder': 'Album Description',
                'rows': 4, 
                'cols': 50,
            }),
            'artist': forms.TextInput(attrs={
                'class': 'formfield',
                'placeholder': 'Artist',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'formfield',
                'placeholder': 'Price',
            }),
            'format': forms.Select(attrs={
                'class': 'formfield',
            }),
            'release_date': forms.DateInput(attrs={
                'class': 'formfield',
                'type': 'date',
            }),
            'cover_art': forms.ClearableFileInput(attrs={
            'class': 'formfield',
            'accept': 'image/*',
            }),
        }


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'runtime', 'albums']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'formfield',
                'placeholder': 'Song Title',
            }),
            'runtime': forms.NumberInput(attrs={
                'class': 'formfield',
                'placeholder': 'Runtime',
            }),
            'albums': forms.CheckboxSelectMultiple(),
        }
 

