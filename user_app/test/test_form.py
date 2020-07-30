from django.test import TestCase
from user_app.forms import UserPurBeurreForm


class TestForm(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_form_isvalid(self):
        """
        verify the form is valid
        """
        form = UserPurBeurreForm(data={
            'email': 'toto@toto.fr',
            'password': 'totototo',
            'confirm_password': 'totototo',
            'connexion_creation': 'creation'
        })
        self.assertTrue(form.is_valid())

    def test_form_isnotvalid(self):
        """
        verify the form is not valid (psw don't match)
        """
        form = UserPurBeurreForm(data={
            'email': 'toto@toto.fr',
            'password': 'totototo',
            'confirm_password': 'titititi',
            'connexion_creation': 'creation'
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
