from django import forms


class ShortLinkForm(forms.Form):
    link = forms.CharField(widget=forms.TextInput({
        'placeholder': 'Write your link here',
        'label': ''}))
