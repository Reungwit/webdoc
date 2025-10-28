from django.test import TestCase, Client
from django.urls import reverse
from .models import CustomUser, DocCover, SpProject, SpProjectAuthor, Abstract, Certificate, Chapter1, RefWebsite
import json
from unittest.mock import patch

class BackendViewsTestCase(TestCase):
    def setUp(self):
        """Set up a test user and client."""
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123',
            full_name='Test User'
        )
        self.client = Client()
        self.client.login(email='test@example.com', password='testpassword123')

    def test_register_view(self):
        """Test user registration view."""
        # Test GET
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

        # Test POST - successful registration
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'full_name': 'New User',
            'email': 'new@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        }, follow=True)
        self.assertRedirects(response, reverse('index'))
        self.assertTrue(CustomUser.objects.filter(username='newuser').exists())

    def test_login_view(self):
        """Test user login view."""
        # Log out first
        self.client.logout()
        
        # Test GET
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        # Test POST - successful login
        response = self.client.post(reverse('login'), {
            'email': 'test@example.com',
            'password': 'testpassword123',
        })
        self.assertRedirects(response, reverse('index'))
        
        # Test POST - failed login
        response = self.client.post(reverse('login'), {
            'email': 'test@example.com',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)

    def test_logout_view(self):
        """Test user logout view."""
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
        # Check user is logged out
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('index')}")

    def test_index_view_authenticated(self):
        """Test index view for authenticated user."""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_index_view_unauthenticated(self):
        """Test index view for unauthenticated user."""
        self.client.logout()
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('index')}")

    def test_doc_cover_view(self):
        """Test document cover view for saving, retrieving, and generating."""
        url = reverse('cover')
        
        # Test GET
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cover.html')

        # Test POST - save_cover
        cover_data = {
            'name_pro_th': 'โครงงานไทย',
            'name_pro_en': 'Project English',
            'name_author_th_1': 'ผู้จัดทำ 1',
            'name_author_th_2': 'ผู้จัดทำ 2',
            'name_author_en_1': 'Author 1',
            'name_author_en_2': 'Author 2',
            'academic_year': '2567',
            'action': 'save_cover'
        }
        response = self.client.post(url, cover_data)
        self.assertEqual(response.status_code, 200) # It renders the page again
        self.assertTrue(DocCover.objects.filter(user=self.user, project_name_th='โครงงานไทย').exists())

        # Test POST - get_data_cover
        response = self.client.post(url, {'action': 'get_data_cover'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cover.html')
        self.assertEqual(response.context['initial']['name_pro_th'], 'โครงงานไทย')

        # Test POST - generate_cover_th
        response = self.client.post(url, {**cover_data, 'action': 'generate_cover_th'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        self.assertIn('attachment; filename=cover_th.docx', response['Content-Disposition'])

        # Test POST - generate_cover_en
        response = self.client.post(url, {**cover_data, 'action': 'generate_cover_en'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        self.assertIn('attachment; filename=cover_en.docx', response['Content-Disposition'])

        # Test POST - generate_cover_sec
        response = self.client.post(url, {**cover_data, 'action': 'generate_cover_sec'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        self.assertIn('attachment; filename=cover_sec.docx', response['Content-Disposition'])

    def test_sp_project_form_view(self):
        """Test SP-01 project form view."""
        url = reverse('sp_project_form')
        
        # Test GET
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sp_project_form.html')

        # Test POST - save
        project_data = {
            'name_pro_th': 'โครงงานพิเศษ',
            'name_pro_en': 'Special Project',
            'case_stu': 'Case Study',
            'term': '1',
            'school_y': '2567',
            'adviser': 'Adviser Name',
            'co_advisor': 'Co-Adviser Name',
            'strategic': 'Strategic Info',
            'plan': 'Plan Info',
            'key_result': 'Key Result Info',
            'bg_and_sig_para1': 'Para 1',
            'bg_and_sig_para2': 'Para 2',
            'bg_and_sig_para3': 'Para 3',
            'purpose_1': 'Purpose 1',
            'purpose_2': 'Purpose 2',
            'purpose_3': 'Purpose 3',
            'name_author_th_1': 'ผู้จัดทำ 1',
            'name_author_th_2': 'ผู้จัดทำ 2',
            'scope_count': '1',
            'scope_b_1': 'Main Scope',
            'scope_subcount_1': '1',
            'scope_s_1_1': 'Sub Scope',
            'action': 'save'
        }
        response = self.client.post(url, project_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(SpProject.objects.filter(user=self.user, name_pro_th='โครงงานพิเศษ').exists())
        project = SpProject.objects.get(user=self.user, name_pro_th='โครงงานพิเศษ')
        self.assertEqual(SpProjectAuthor.objects.filter(project=project).count(), 2)

        # Test POST - get_data
        response = self.client.post(url, {'action': 'get_data'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sp_project_form.html')
        self.assertEqual(response.context['initial']['name_pro_th'], 'โครงงานพิเศษ')

        # Test POST - generate
        response = self.client.post(url, {**project_data, 'action': 'generate'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        self.assertIn('attachment; filename=sp_project_form.docx', response['Content-Disposition'])

    def test_certificate_view(self):
        """Test certificate view for saving, retrieving, and generating."""
        url = reverse('certificate')
        
        # Test GET
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'certificate.html')

        # Test POST - save_certificate
        cert_data = {
            'topic': 'Test Topic',
            'author1': 'Author 1',
            'author2': 'Author 2',
            'dean': 'Dean Name',
            'chairman': 'Chairman Name',
            'committee1': 'Committee 1',
            'committee2': 'Committee 2',
            'action': 'save_certificate'
        }
        response = self.client.post(url, cert_data, follow=True)
        self.assertRedirects(response, url)
        self.assertTrue(Certificate.objects.filter(user=self.user, topic='Test Topic').exists())

        # Test POST - get_certificate
        response = self.client.post(url, {'action': 'get_certificate'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Certificate.html')
        self.assertEqual(response.context['initial']['topic'], 'Test Topic')

        # Test POST - generate_certificate
        response = self.client.post(url, {**cert_data, 'action': 'generate_certificate'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/octet-stream') # FileResponse
        self.assertIn('attachment; filename=certificate.docx', response['Content-Disposition'])
