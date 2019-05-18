from django.db import models
from django import forms
from django.forms import ClearableFileInput

# for deleting media files after record is deleted
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

class UserDetails(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    name            = models.CharField('Name', max_length=255, null=True, blank=True)
    email           = models.EmailField('Email', max_length=255, null=True, blank=True)
    mobile_number   = models.IntegerField('Mobile Number', null=True, blank=True)
    skills          = models.CharField('Skills', max_length=1000, null=True, blank=True)
    years_of_exp    = models.FloatField('Experience', null=True, blank=True)
    
    def __str__(self):
        return self.user.get_full_name()

class Competencies(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    competency      = models.CharField('Competency', max_length=1000, null=True, blank=True)
    
    def __str__(self):
        return self.user.get_full_name()

class MeasurableResults(models.Model):
    user              = models.ForeignKey(User, on_delete=models.CASCADE)
    measurable_result = models.CharField('Competency', max_length=1000, null=True, blank=True)
    
    def __str__(self):
        return self.user.get_full_name()

class Resume(models.Model):
    user              = models.ForeignKey(User, on_delete=models.CASCADE)
    resume            = models.FileField('Upload Resumes', upload_to='resumes/')
    last_uploaded_on  = models.DateTimeField('Uploaded On', auto_now_add=True)

    def __str__(self):
        return self.user.email

class ResumeDetails(models.Model):
    resume      = models.ForeignKey(Resume, on_delete=models.CASCADE)
    page_nos    = models.IntegerField('Number of Pages', null=True, blank=True)
    
    def __str__(self):
        return self.resume.user.email

class UploadResumeModelForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['resume']
        widgets = {
            'resume': ClearableFileInput(attrs={'multiple': True}),
        }

# delete the resume files associated with each object or record
@receiver(post_delete, sender=Resume)
def submission_delete(sender, instance, **kwargs):
    instance.resume.delete(False)
