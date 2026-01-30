from django import forms
from .models import Job, Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'contact_person', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Client Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email (Optional)'}),
            'contact_person': forms.TextInput(attrs={'placeholder': 'Contact Person (Optional)'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone (Optional)'}),
        }

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'client', 'status', 'min_experience', 'max_experience', 
                  'budget_min', 'budget_max', 'location', 'skills_required']
        widgets = {
            'skills_required': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Python, Django, AWS...'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(JobForm, self).__init__(*args, **kwargs)
        if user and user.role == "CLIENT":
            # Clients can't change the client field (it's them)
            self.fields.pop('client') 

class JobSearchForm(forms.Form):
    q = forms.CharField(required=False, label='Search', widget=forms.TextInput(attrs={'placeholder': 'Search jobs...', 'class': 'form-control'}))
    status = forms.ChoiceField(choices=[('', 'All Status')] + list(Job.STATUS_CHOICES), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
