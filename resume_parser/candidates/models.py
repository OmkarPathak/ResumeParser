from django.db import models
from django.conf import settings
from jobs.models import Job

class Candidate(models.Model):
    ACTIVE = 'ACTIVE'
    PAUSED = 'PAUSED'
    PLACED = 'PLACED'
    
    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (PAUSED, 'Paused'),
        (PLACED, 'Placed'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='candidate_profile')
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True, db_index=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    resume_file = models.FileField(upload_to='resumes/')
    
    # Parsed Data
    skills = models.TextField(blank=True, null=True, help_text="Parsed skills")
    experience_years = models.IntegerField(default=0)
    education = models.TextField(blank=True, null=True)
    ai_summary = models.TextField(blank=True, null=True, help_text="AI Generated Summary")
    ai_strengths = models.TextField(blank=True, null=True, help_text="Key Strengths")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ACTIVE, db_index=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='added_candidates')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    # Compatibility Properties for Template (Adapter Removal)
    @property
    def tag(self):
        return self.status
        
    @property
    def mobile_number(self):
        return self.phone
        
    @property
    def uploaded_on(self):
        return self.created_at

    processing_time = models.FloatField(default=0.0, help_text="Time taken to parse in seconds")
    remark = models.CharField(max_length=1000, blank=True, null=True)

    @property
    def latest_experience(self):
        return self.experiences.first()

class Application(models.Model):
    APPLIED = 'APPLIED'
    SCREENED = 'SCREENED'
    INTERVIEW = 'INTERVIEW'
    OFFERED = 'OFFERED'
    REJECTED = 'REJECTED'
    HIRED = 'HIRED'
    
    STATUS_CHOICES = (
        (APPLIED, 'Applied'),
        (SCREENED, 'Screened'),
        (INTERVIEW, 'Interviewing'),
        (OFFERED, 'Offered'),
        (REJECTED, 'Rejected'),
        (HIRED, 'Hired'),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=APPLIED, db_index=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('job', 'candidate')

    def __str__(self):
        return f"{self.candidate.name} -> {self.job.title}"

class Interview(models.Model):
    ROUND_CHOICES = (
        ('SCREENING', 'Screening'),
        ('TECHNICAL', 'Technical'),
        ('MANAGERIAL', 'Managerial'),
        ('HR', 'HR Round'),
        ('FINAL', 'Final Decision'),
    )
    
    STATUS_CHOICES = (
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('PASSED', 'Passed'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    )

    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='interviews')
    interviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    round_name = models.CharField(max_length=20, choices=ROUND_CHOICES, default='SCREENING')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    date_time = models.DateTimeField()
    link = models.URLField(blank=True, null=True, help_text="Zoom/Meet Link")
    notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.round_name} - {self.application.candidate.name}"

class Experience(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='experiences')
    designation = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    job_description = models.TextField(blank=True, null=True)
    start_date = models.CharField(max_length=100, blank=True, null=True)
    end_date = models.CharField(max_length=100, blank=True, null=True)
    is_current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.designation} at {self.company}"
