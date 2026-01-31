from django.test import TestCase
from django.contrib.auth import get_user_model
from jobs.models import Job, Client

User = get_user_model()

class JobModelTest(TestCase):
    def setUp(self):
        self.recruiter = User.objects.create_user(username='recruiter', password='password', role='RECRUITER')
        self.client = Client.objects.create(
            name="Tech Corp", 
            contact_person="Jane Doe", 
            email="jane@tech.com",
            owner=self.recruiter
        )
        
    def test_job_creation(self):
        """Test creating a job"""
        job = Job.objects.create(
            title="Senior Engineer",
            client=self.client,
            # description="Great role", # Removed
            location="Remote",
            budget_min=100000,
            budget_max=150000,
            skills_required="Python, Django",
            created_by=self.recruiter
        )
        self.assertEqual(job.title, "Senior Engineer")
        self.assertEqual(job.client, self.client)
        self.assertEqual(job.status, 'DRAFT') # Default is DRAFT
        
    def test_job_defaults(self):
        """Test default values for job"""
        job = Job.objects.create(
            title="Junior Dev",
            client=self.client,
            created_by=self.recruiter
        )
        self.assertEqual(job.status, 'DRAFT')
