
from django import forms


class LinkInputForm(forms.Form):

    css_parameters = { 'placeholder': 'Place your link here!',
                      
                      'class': 'searchInput'}
    Enter_a_Valid_Link = forms.CharField(max_length = 800, widget= forms.TextInput(attrs=css_parameters))

