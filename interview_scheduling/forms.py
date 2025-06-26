# from django import forms
# from .models import InterviewSession
# from questions.models import Field
# from datetime import datetime

# class InterviewSessionForm(forms.ModelForm):
#     scheduled_date = forms.DateField(
#         widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#         label="Scheduled Date"
#     )
#     scheduled_time = forms.TimeField(
#         widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
#         label="Scheduled Time"
#     )
#     ended_date = forms.DateField(
#         widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#         label="End Date"
#     )
#     ended_time = forms.TimeField(
#         widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
#         label="End Time"
#     )

#     selected_fields = forms.ModelMultipleChoiceField(
#         queryset=Field.objects.none(),
#         widget=forms.CheckboxSelectMultiple,
#         required=False,
#         label="Choose Fields to Generate Questions From"
#     )

#     class Meta:
#         model = InterviewSession
#         fields = ['job', 'status', 'duration_minutes', 'scheduled_at', 'ended_at']
#         widgets = {
#             'job': forms.Select(attrs={'class': 'form-control'}),
#             'status': forms.Select(attrs={'class': 'form-control'}),
#             'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
#         }

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         super().__init__(*args, **kwargs)

#         # hide original datetime fields
#         self.fields['scheduled_at'].widget = forms.HiddenInput()
#         self.fields['ended_at'].widget = forms.HiddenInput()

#         if user:
#             self.fields['selected_fields'].queryset = Field.objects.filter(created_by=user)

#         # Pre-fill date/time fields if editing
#         if self.instance and self.instance.pk:
#             self.initial['scheduled_date'] = self.instance.scheduled_at.date()
#             self.initial['scheduled_time'] = self.instance.scheduled_at.time()
#             self.initial['ended_date'] = self.instance.ended_at.date()
#             self.initial['ended_time'] = self.instance.ended_at.time()

    
from django import forms
from .models import InterviewSession
from questions.models import Field  

class InterviewSessionForm(forms.ModelForm):
    selected_fields = forms.ModelMultipleChoiceField(
        queryset=Field.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Select Question Fields"
    )

    class Meta:
        model = InterviewSession
        fields = ['job', 'duration_minutes', 'status', 'scheduled_at', 'ended_at']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Limit jobs shown to only those posted by this user, if needed
            self.fields['job'].queryset = self.fields['job'].queryset.filter(created_by=user)
