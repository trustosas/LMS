from django.contrib.auth import get_user_model
from django.test import TestCase


class UserModelTests(TestCase):
    def test_user_roles(self):
        User = get_user_model()
        u = User.objects.create_user(username="x", password="y", role="LIBRARIAN")
        self.assertTrue(u.is_librarian())
        self.assertFalse(u.is_admin())


