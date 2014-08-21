from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML, Submit

from django.core.urlresolvers import reverse

class SurveyForm(forms.Form):
    person_types = forms.MultipleChoiceField(
        label = 'Check every term that best descibe you',
        widget=forms.CheckboxSelectMultiple,
        choices = (
            ('Patient','Patient'),
            ('Medical Provider','Medical Provider'),
            ('Caregiver','Caregiver'),
            ('Designer','Designer'),
            ('Technologist','Technologist'),
            ),
        )
    birth_year = forms.CharField(
        label = 'Enter your birth year',
        help_text= 'Enter the year in YYYY format',
        )
    def __init__(self, data=None, session=None, *args, **kwargs):
        if data:
            super(SurveyForm, self).__init__(data, *args, **kwargs)
        else:
            super(SurveyForm, self).__init__(*args, **kwargs)
        if session:
            self.session = session
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('main-survey')
        self.helper.add_input(Submit('submit', 'Submit'))

    def clean(self):
        cleaned_data = super(SurveyForm, self).clean()
        if 'birth_year' not in cleaned_data:
            return cleaned_data
        birth_year = cleaned_data['birth_year']
        if len(birth_year) != 4:
            self._errors['birth_year'] = self.error_class(['Please enter only 4 digits'])
            del cleaned_data['birth_year']
        try:
            birth_year = int(birth_year)
        except:
            self._errors['birth_year'] = self.error_class(['Please enter only numbers'])
            del cleaned_data['birth_year']
        return cleaned_data



class EmailForm(forms.Form):
    email = forms.CharField(required=True, widget=forms.EmailInput)

    def __init__(self, data=None, session=None, *args, **kwargs):
        if data:
            super(EmailForm, self).__init__(data, *args, **kwargs)
        else:
            super(EmailForm, self).__init__(*args, **kwargs)
        if session:
            self.session = session
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('main-email')

        if self.session and self.session.user:
            self.helper.layout = Layout(
                HTML("<p>Thanks for giving us your email. You should recieve an email from us shortly.</p>"),
                )
        else:
            self.helper.layout = Layout(
                'email',
                Submit('submit','Add your email')
                )