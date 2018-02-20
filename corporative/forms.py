from django import forms


class ContactForm(forms.Form):
    subject = forms.CharField(
        label='subject',
    )

    phone = forms.CharField(
        required=False,
        label='phone',
    )

    name = forms.CharField(
        label='name',
    )

    email = forms.EmailField(
        label='email',
    )

    message = forms.CharField(
        label='message',
        widget=forms.Textarea,
    )

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

        if request.user.is_authenticated:
            self.fields['name'].widget.attrs['readonly'] = True
            self.fields['email'].widget.attrs['readonly'] = True
