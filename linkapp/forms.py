from django import forms

    # This file describes forms, that render
    # on pages


class ShortLinkForm(forms.Form):
    """ Class which describes form for ShortLink creation
    """
    link = forms.CharField(widget=forms.TextInput({  # Field for user's full link
        'placeholder': ' Write your link here',       # Corresponds to ShotLink model's full link field
        'label': ''}))
