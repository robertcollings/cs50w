from django import forms
from .models import Categories


class CreateListingForm(forms.Form):
    title = forms.CharField(label='Listing title', max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    start_bid = forms.DecimalField(decimal_places=2, min_value=0, label='Starting bid')
    image = forms.URLField(label="URL to image")
    category = forms.ModelChoiceField(queryset=Categories.objects.all().order_by('category'))

class CreateBidForm(forms.Form):
    amount = forms.DecimalField(label='', decimal_places=2, min_value=0)

class CreateCommentsForm(forms.Form):
    comment = forms.CharField(max_length=1024, label="Add a comment:")