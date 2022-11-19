
from django import forms


class LinkInputForm(forms.Form):
    Enter_a_Valid_Link = forms.CharField(max_length = 500, widget= forms.TextInput(attrs={ "style":"width:250px;margin:4px;margin-left:20px;font-size: large"}))

