from django.http import response
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


# Create your tests here.
class OrderViewTestCase(TestCase):
    """
    test order view
    """

    def setUp(self):
        return super().setUp()

    def test_auth_require(self):
        """
        Test of view redirect anonymose to login page
        """
        response = self.client.get(reverse("orders"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        response = self.client.get(reverse("orders"), follow=True)
        self.assertContains(response, "Please login")

    def test_user_empty_cart(self):
        user = get_user_model().objects.create(username="user1")
        self.client.force_login(user=user)
        response = self.client.get(reverse("orders"))
        self.assertEquals(response.context_data["paginator"].count, 0)
