from django import forms
from .models import Candidate, Interview

class CandidateUploadForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['resume_file']
        widgets = {
            'resume_file': forms.ClearableFileInput(attrs={'accept': '.pdf,.docx,.doc,application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document'}),
        }

class CandidateUpdateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['name', 'email', 'phone', 'skills', 'experience_years', 'education']
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 4}),
            'education': forms.Textarea(attrs={'rows': 4}),
        }

class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['round_name', 'status', 'date_time', 'link', 'interviewer', 'notes']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
