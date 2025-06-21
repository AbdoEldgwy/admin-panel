
from django import forms
from .models import InterviewSession

class InterviewSessionForm(forms.ModelForm):
    class Meta:
        model = InterviewSession
        fields = '__all__'