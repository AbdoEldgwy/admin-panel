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

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Field.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError('A field with this name already exists.')
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

    # def __init__(self, *args, **kwargs):
    #     field_instance = kwargs.pop('field_instance', None) 

    #     super().__init__(*args, **kwargs)
    #     # if field_instance:
    #         # self.fields['field'].initial = field_instance
    #         # self.fields['field'].widget = forms.HiddenInput()  

    #     self.fields['level'].help_text = 'Choose the difficulty level'
    #     self.fields['question_text'].help_text = 'Enter the question text'


    # def clean_question_text(self):
    #     question_text = self.cleaned_data.get('question_text')
    #     if len(question_text.strip()) < 10:
    #         raise forms.ValidationError('Question text must be at least 10 characters long')
    #     return question_text
