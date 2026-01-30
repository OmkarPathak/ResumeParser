from django.test import TestCase
from django.contrib.auth import get_user_model

class UserTests(TestCase):
    def test_create_user_with_roles(self):
        User = get_user_model()
        recruiter = User.objects.create_user(username='recruiter', password='password', role=User.RECRUITER)
        self.assertEqual(recruiter.role, User.RECRUITER)
        
        client = User.objects.create_user(username='client', password='password', role=User.CLIENT)
        self.assertEqual(client.role, User.CLIENT)

    def test_admin_role_assignment(self):
        User = get_user_model()
        admin = User.objects.create_superuser(username='admin_test', password='password', email='admin@test.com')
        self.assertEqual(admin.role, User.ADMIN)
