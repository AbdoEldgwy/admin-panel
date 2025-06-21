from django import forms
from .models import InterviewSession
from questions.models import Field  # تأكد من المسار الصحيح

class InterviewSessionForm(forms.ModelForm):
    selected_fields = forms.ModelMultipleChoiceField(
        queryset=Field.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Choose Fields to Generate Questions From"
    )

    class Meta:
        model = InterviewSession
        fields = ['job', 'status', 'scheduled_at', 'ended_at', 'duration_minutes']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['selected_fields'].queryset = Field.objects.filter(created_by=user)
