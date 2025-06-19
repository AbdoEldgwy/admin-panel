from django import forms
from .models import Question, Field

class FieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter field name'
            })
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Field.objects.filter(name__iexact=name, created_by=self.user).exists():
            raise forms.ValidationError('You already have a field with this name.')
        return name


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'level']
        widgets = {
            'level': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'difficulty level'
            }),
            'question_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Enter your question here...'
            }),
        }
