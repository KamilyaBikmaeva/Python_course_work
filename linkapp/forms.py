from django import forms

'''
    This file describes forms, that render
    on pages
'''

class ShortLinkForm(forms.Form):
    link = forms.CharField(widget=forms.TextInput({
        'placeholder': 'Write your link here',
        'label': ''}))
