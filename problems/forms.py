from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML, Submit

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
        self.helper.form_action = reverse(suggestion)

        self.helper.layout = Layout(
            'description',
            'email',
            HTML("""
                    <nav class="navbar navbar-default navbar-fixed-bottom form-actions">
                        <div class="container">
                            <input class="navbar-btn btn btn-default pull-right" type="submit" name="selected" value="Add Your Suggestion" />
                            <input class="navbar-btn btn pull-right" type="submit" name="skip" value="Skip" />
                        </div>
                    </nav>
                """)
            )
