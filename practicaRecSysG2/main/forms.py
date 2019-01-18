from django import forms

class UserForm(forms.Form):
    id = forms.CharField(label = "User ID")

    
class BookForm(forms.Form):
    isbn = forms.CharField(label = "Book ISBN")