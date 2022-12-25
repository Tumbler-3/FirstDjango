from django import forms
import datetime

class CreateProduct(forms.Form):
    title = forms.CharField(min_length=5)
    description = forms.CharField(widget=forms.Textarea())
    date = forms.DateField(initial=datetime.date.today)


class CreateReview(forms.Form):
    text = forms.CharField(min_length=3, label='comment')
