from django import forms

from users.models import Company


class CreateNewService(forms.Form):
    name = forms.CharField(max_length=40)
    description = forms.CharField(widget=forms.Textarea, label='Description')
    price_hour = forms.DecimalField(
        decimal_places=2, max_digits=5, min_value=0.00)
    field = forms.ChoiceField(required=True)

    def __init__(self, *args, choices='', ** kwargs):
        super(CreateNewService, self).__init__(*args, **kwargs)
        # adding choices to fields
        if choices:
            self.fields['field'].choices = choices
        # adding placeholders to form fields
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Service Name'
        self.fields['description'].widget.attrs['placeholder'] = 'Enter Description'
        self.fields['price_hour'].widget.attrs['placeholder'] = 'Enter Price per Hour'

        self.fields['name'].widget.attrs['autocomplete'] = 'off'

    def clean_price_hour(self):
        price_hour = self.cleaned_data['price_hour']
        if price_hour <= 0:
            raise forms.ValidationError("Price per hour must be a positive number.")
        return price_hour


class RequestServiceForm(forms.Form):
    address = forms.CharField(max_length=100)
    time = forms.IntegerField()

    def clean_time(self):
        time = self.cleaned_data['time']
        if time <= 0:
            raise forms.ValidationError("Service time must be a positive number.")
        return time
