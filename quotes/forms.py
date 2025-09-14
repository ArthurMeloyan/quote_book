from django import forms
from .models import Quote
from django.forms import Textarea, TextInput, NumberInput
class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['text', 'source', 'weight']


        widgets = {
            'text': Textarea(attrs={
                'class': 'quote-input',
                'placeholder': 'Введите цитату, которую хотите добавить'
            }),
            'source': TextInput(attrs={
                'class': 'source-input',
                'placeholder': 'Введите источник'
            }),
            'weight': NumberInput(attrs={
                'class': 'weight-input',
                'placeholder': 'Введите вес цитаты'
            })
        }

        