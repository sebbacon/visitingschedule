from django import forms

class EventForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass


class HelperForm(forms.Form):
    name = forms.CharField()
    email = forms.CharField()
