from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from .models import SupplementRecord
from django.test.utils import override_settings
from django.core.cache import cache

class ViewsTestCase(TestCase):
    def setUp(self):
        cache.clear()  # Clear cache before each test
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        # Create test record
        self.record = SupplementRecord.objects.create(
            user=self.user,
            supplement_name='Test Supplement',
            amount=1,
            intake_datetime='2024-03-21 10:00:00'
        )

    def tearDown(self):
        cache.clear()  # Clear cache after each test

    @override_settings(RATELIMIT_ENABLE=False)
    def test_login_view(self):
        """Test successful login"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('supplement_record'))

    @override_settings(RATELIMIT_ENABLE=False)
    def test_failed_login(self):
        """Test login failure with incorrect credentials"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)

        # Check for error message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(len(messages) > 0, "No messages found")
        self.assertTrue(
            any(message.message == "Invalid username or password." for message in messages),
            "Expected error message not found"
        )

    def test_supplement_record_view(self):
        # Login first
        self.client.login(username='testuser', password='testpass123')
        # Test GET request
        response = self.client.get(reverse('supplement_record'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/supplement_record.html')

    def test_edit_record(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('edit_record', kwargs={'record_id': self.record.id}),
            {
                'supplement_name': 'Updated Supplement',
                'amount': 2,
                'intake_datetime': '2024-03-21 11:00:00'
            }
        )
        self.assertEqual(response.status_code, 302)
        updated_record = SupplementRecord.objects.get(id=self.record.id)
        self.assertEqual(updated_record.supplement_name, 'Updated Supplement')

    def test_delete_record(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('delete_record', kwargs={'record_id': self.record.id})
        )
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(SupplementRecord.DoesNotExist):
            SupplementRecord.objects.get(id=self.record.id)

class RateLimitTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    @override_settings(RATELIMIT_ENABLE=True)
    def test_login_rate_limit(self):
        # Make 6 requests (rate limit is 5/minute)
        for _ in range(6):
            response = self.client.post(reverse('login'), {
                'username': 'testuser',
                'password': 'wrongpass'
            })
        self.assertEqual(response.status_code, 403)  # Should be rate limited
