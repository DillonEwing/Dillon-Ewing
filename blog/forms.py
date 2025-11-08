# blog/forms.py

from django import forms

class CommentForm(forms.Form):
    # author is optional because logged-in users will be used instead
    author = forms.CharField(
        max_length=60,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your Name"}
        ),
    )
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Leave a comment!"}
        )
    )