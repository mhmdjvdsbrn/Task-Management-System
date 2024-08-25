# Inside task_backend/users/tests/test_models.py

from django.test import TestCase
from django.core.exceptions import ValidationError
from task_backend.users.models import BaseUser, Profile
from task_backend.users.validators import validate_phone_number, number_validator, letter_validator, special_char_validator

class TestBaseUserModel(TestCase):

    def setUp(self):
        self.phone = '09123456789'
        self.email = 'user@example.com'
        self.password = 'StrongPass123!'

    def test_create_user_success(self):
        user = BaseUser.objects.create_user(phone=self.phone, password=self.password)
        self.assertIsInstance(user, BaseUser)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_admin)
        self.assertEqual(user.phone, self.phone)

    def test_create_superuser_success(self):
        user = BaseUser.objects.create_superuser(phone=self.phone, password=self.password)
        self.assertIsInstance(user, BaseUser)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_admin)
        self.assertTrue(user.is_superuser)

    def test_create_user_no_phone_raises_error(self):
        with self.assertRaises(ValueError):
            BaseUser.objects.create_user(phone=None, password=self.password)

    def test_create_user_no_password_sets_unusable_password(self):
        user = BaseUser.objects.create_user(phone=self.phone, password=None)
        self.assertFalse(user.has_usable_password())

    def test_is_staff_property(self):
        user = BaseUser.objects.create_user(phone=self.phone, password=self.password)
        self.assertFalse(user.is_staff())
        user.is_admin = True
        self.assertTrue(user.is_staff())

    def test_phone_unique_constraint(self):
        BaseUser.objects.create_user(phone=self.phone, password=self.password)
        with self.assertRaises(ValidationError):
            user2 = BaseUser(phone=self.phone)
            user2.full_clean()

    def test_email_nullability(self):
        user = BaseUser.objects.create_user(phone=self.phone, password=self.password)
        self.assertIsNone(user.email)
        user.email = self.email
        user.save()
        self.assertEqual(user.email, self.email)

    def test_str_representation(self):
        user = BaseUser.objects.create_user(phone=self.phone, password=self.password)
        self.assertEqual(str(user), self.phone)

class TestProfileModel(TestCase):

    def setUp(self):
        self.phone = '09123456789'
        self.user = BaseUser.objects.create_user(phone=self.phone, password='StrongPass123!')
        self.first_name = 'javad'
        self.last_name = 'sbrn'
        self.gender = Profile.MALE

    def test_profile_creation(self):
        profile = Profile.objects.create(user=self.user, first_name=self.first_name, last_name=self.last_name, gender=self.gender)
        self.assertIsInstance(profile, Profile)
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.first_name, self.first_name)
        self.assertEqual(profile.last_name, self.last_name)
        self.assertEqual(profile.gender, self.gender)

    def test_avatar_default_value(self):
        profile = Profile.objects.create(user=self.user, first_name=self.first_name, last_name=self.last_name, gender=self.gender)
        self.assertEqual(profile.avatar, 'images/profiles/avatar.jpg')

    def test_gender_choices(self):
        profile = Profile.objects.create(user=self.user, first_name=self.first_name, last_name=self.last_name, gender=Profile.FEMALE)
        self.assertEqual(profile.gender, Profile.FEMALE)
        with self.assertRaises(ValidationError):
            profile.gender = 'Invalid'
            profile.full_clean()

    def test_get_profile_avatar_path(self):
        profile = Profile.objects.create(user=self.user, first_name=self.first_name, last_name=self.last_name, gender=self.gender)
        filename = 'avatar.png'
        expected_path = f'images/profiles/{self.first_name}_{self.last_name}/{filename}'
        self.assertEqual(profile.avatar.field.upload_to(profile, filename), expected_path)

class TestValidators(TestCase):

    def test_validate_phone_number_success(self):
        phone = '09123456789'
        validate_phone_number(phone)  # Should not raise any exception

    def test_number_validator_success(self):
        password = 'abc123'
        number_validator(password)  # Should not raise any exception

    def test_number_validator_no_number(self):
        with self.assertRaises(ValidationError):
            number_validator('abcdef')

    def test_letter_validator_success(self):
        password = 'abc123'
        letter_validator(password)  # Should not raise any exception

    def test_letter_validator_no_letter(self):
        with self.assertRaises(ValidationError):
            letter_validator('123456')

    def test_special_char_validator_success(self):
        password = 'abc123!'
        special_char_validator(password)  # Should not raise any exception

    def test_special_char_validator_no_special_char(self):
        with self.assertRaises(ValidationError):
            special_char_validator('abc123')
