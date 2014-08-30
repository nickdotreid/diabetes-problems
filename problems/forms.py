from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML, Submit

from django.core.urlresolvers import reverse

class SuggestionForm(forms.Form):
    description = forms.CharField(
        label="Describe your issue",
        help_text='Tell us about the context about the issue. When does the issues happen? Who is involved?',
        required=True,
        widget = forms.Textarea,
        )
    email = forms.CharField(
        label="Add your email address so we can clarify anything we don't understand in your issue (Optional)",
        required=False,
        widget=forms.EmailInput,
        )

    def __init__(self, *args, **kwargs):
        super(SuggestionForm,self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('suggestion-add')

        self.helper.attrs = {
            'data_target':'pane',
        }

        self.helper.layout = Layout(
            'description',
            'email',
            Div(
                Submit("submit","Add Your Issue", css_class="btn-primary btn-large pull-right"),
                Submit("skip","Not now", css_class="btn-secondary btn-large pull-right"),
                css_class="form-actions")
            )
