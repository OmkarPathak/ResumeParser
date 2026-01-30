from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Candidate, Application
from jobs.models import Job, Client

class CandidateFlowTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.recruiter = User.objects.create_user(username='recruiter', password='password', role=User.RECRUITER)
        
        # Setup Job
        self.client = Client.objects.create(name='Test Client', owner=self.recruiter)
        self.job = Job.objects.create(
            title='Software Engineer',
            client=self.client,
            created_by=self.recruiter,
            status=Job.ACTIVE
        )

    def test_candidate_creation(self):
        resume_file = SimpleUploadedFile("resume.txt", b"dummy content")
        candidate = Candidate.objects.create(
            name="John Doe",
            email="john@example.com",
            resume_file=resume_file,
            created_by=self.recruiter
        )
        self.assertEqual(candidate.status, Candidate.ACTIVE)

    def test_submission(self):
        resume_file = SimpleUploadedFile("resume.txt", b"dummy content")
        candidate = Candidate.objects.create(
            name="Jane Doe",
            created_by=self.recruiter
        )
        
        # Submit
        app = Application.objects.create(candidate=candidate, job=self.job)
        self.assertEqual(app.status, Application.APPLIED)
        self.assertEqual(app.job.title, 'Software Engineer')
