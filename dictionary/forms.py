from django import forms
from .models import Word, Grammar


class WordForm(forms.ModelForm):

    class Meta:
        model = Word
        fields = ['text', 'translation', 'related_words']
        labels = {
            'text': 'Bosnian Word',
            'translation': 'Arabic Translation',
            'related_words': 'Related Words',
        }


class GrammarForm(forms.ModelForm):
    class Meta:
        model = Grammar
        fields = ['content']
