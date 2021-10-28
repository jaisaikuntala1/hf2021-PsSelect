from django.forms import ModelForm
from .models import ProblemStatement


class PSForm(ModelForm):
    class Meta:
        model = ProblemStatement
        fields = '__all__'
        exclude = ['count']

    def __init__(self, *args, **kwargs):
        super(PSForm, self).__init__(*args, **kwargs)
        self.fields['probNo'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['psname'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['description'].widget.attrs.update(
            {'class': 'form-control'})

class UpdatePSForm(ModelForm):
    class Meta:
        model = ProblemStatement
        fields = '__all__'
        exclude = ['count']

    def __init__(self, *args, **kwargs):
        super(UpdatePSForm, self).__init__(*args, **kwargs)
        self.fields['probNo'].widget.attrs['readonly'] = True
        self.fields['probNo'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['psname'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['description'].widget.attrs.update(
            {'class': 'form-control'})
