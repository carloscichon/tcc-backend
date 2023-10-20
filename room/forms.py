from django import forms

class RoomForm(forms.ModelForm):
    passwd = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Room