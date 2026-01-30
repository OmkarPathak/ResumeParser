from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Client, Job

class JobTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.recruiter = User.objects.create_user(username='recruiter', password='password', role=User.RECRUITER)
        self.client = Client.objects.create(name='Test Client', owner=self.recruiter)

    def test_job_creation(self):
        job = Job.objects.create(
            title='Software Engineer',
            client=self.client,
            created_by=self.recruiter,
            min_experience=2,
            max_experience=5,
            skills_required='Python, Django'
        )
        self.assertEqual(job.title, 'Software Engineer')
        self.assertEqual(job.client, self.client)
        self.assertEqual(job.status, Job.DRAFT)
