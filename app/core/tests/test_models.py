from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='nikhil@nikhil.com', password='nikhil123'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successfully(self):
        """Test to check whether user created successfully with email"""
        email = 'nikhil@nikhil.com'
        password = 'Password123'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test new user email is normalized"""
        email = "nikhil@NIKHIL.COM"
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test new user invalid email raises value error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_new_superuser_create(self):
        """Test new superuser is created"""
        user = get_user_model().objects.create_superuser(
            'nikhil@nikhil.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag str representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient str representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_model_str(self):
        """Test recipe str representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Steak and Mushroom Sauce',
            time_minutes=5,
            price=2.00
        )

        self.assertEqual(str(recipe), recipe.title)
