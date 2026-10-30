"""Forms with validation for the polling app."""
from django import forms

from .models import Choice


class VoteForm(forms.Form):
    """A single required radio-button choice, limited to one question's choices."""
    choice = forms.ModelChoiceField(
        queryset=Choice.objects.none(),
        widget=forms.RadioSelect,
        empty_label=None,
        error_messages={
            'required': 'Please select a choice before voting.',
            'invalid_choice': 'That choice is not valid for this poll.',
        },
    )

    def __init__(self, question, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only accept choices that belong to THIS question (blocks tampered POSTs)
        self.fields['choice'].queryset = question.choices.all()
