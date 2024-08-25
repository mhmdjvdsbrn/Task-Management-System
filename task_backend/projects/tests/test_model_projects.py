from django.test import TestCase
from django.contrib.auth import get_user_model
from task_backend.projects.models import Task
from django.core.exceptions import ValidationError

User = get_user_model()

class TaskModelTests(TestCase):

    def setUp(self):
        """Create a user and a task instance for testing"""
        self.user = User.objects.create_user(phone="09123456789", password="StrongP@ssword1")
        self.task = Task.objects.create(
            title='Test Task',
            description='This is a test task',
            status='in_progress',
            user=self.user
        )

    def test_task_creation(self):
        """Test that the task is created with the correct attributes"""
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.description, 'This is a test task')
        self.assertEqual(self.task.status, 'in_progress')
        self.assertEqual(self.task.user, self.user)
        self.assertIsNotNone(self.task.created_at)
        self.assertIsNotNone(self.task.updated_at)
    
    def test_default_status(self):
        """Test that the default status is 'in_progress'"""
        task = Task.objects.create(
            title='New Task',
            user=self.user
        )
        self.assertEqual(task.status, 'in_progress')

    def test_string_representation(self):
        """Test the string representation of the task"""
        self.assertEqual(str(self.task), 'Test Task')

    def test_task_update(self):
        """Test that updating the task updates the `updated_at` field"""
        old_updated_at = self.task.updated_at
        self.task.title = 'Updated Task'
        self.task.save()
        self.assertNotEqual(self.task.updated_at, old_updated_at)
    
    def test_task_status_choices(self):
        """Test that task status choices are correct"""
        task = Task(title='Status Test Task', user=self.user)
        
        # Test valid status
        task.status = 'completed'
        try:
            task.full_clean()  # This will validate the model
            task.save()
        except ValidationError:
            self.fail('ValidationError raised for valid status')

        # Test invalid status
        task.status = 'invalid_status'
        with self.assertRaises(ValidationError):
            task.full_clean()  # This should raise ValidationError

    def test_task_user_relationship(self):
        """Test the user foreign key relationship"""
        self.assertEqual(self.task.user.phone, '09123456789')

