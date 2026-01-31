from django.test import TestCase
from django.contrib.auth import get_user_model
from candidates.models import Candidate, Application
from jobs.models import Job, Client

User = get_user_model()

class CandidateModelTest(TestCase):
    def setUp(self):
        # Create Users
        self.candidate_user = User.objects.create_user(username='testcandidate', password='password', role='CANDIDATE')
        self.recruiter_user = User.objects.create_user(username='testrecruiter', password='password', role='RECRUITER')
        
    def test_candidate_creation(self):
        """Test creating a candidate linked to a user"""
        candidate = Candidate.objects.create(
            user=self.candidate_user,
            name="Test Candidate",
            email="test@example.com",
            phone="1234567890",
            created_by=self.candidate_user
        )
        self.assertEqual(candidate.name, "Test Candidate")
        self.assertEqual(candidate.user, self.candidate_user)
        self.assertEqual(str(candidate), "Test Candidate")

    def test_application_logic(self):
        """Test applying for a job"""
        # Setup Job
        client = Client.objects.create(
            name="Test Client", 
            contact_person="John Doe",
            owner=self.recruiter_user  # Added owner
        )
        job = Job.objects.create(
            title="Senior Developer",
            client=client,
            # description="Good job", # Removed as not in model
            created_by=self.recruiter_user
        )
        
        candidate = Candidate.objects.create(
            user=self.candidate_user,
            name="Applicant",
            email="apply@example.com",
            created_by=self.candidate_user
        )
        
        application = Application.objects.create(
            job=job,
            candidate=candidate,
            status='APPLIED'
        )
        
        self.assertEqual(application.job, job)
        self.assertEqual(application.candidate, candidate)
        self.assertEqual(application.status, 'APPLIED')
