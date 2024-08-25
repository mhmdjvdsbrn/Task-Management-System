from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from task_backend.projects.models import Task

User = get_user_model()

class TaskViewSetTests(APITestCase):

    def setUp(self):
        """Create a user and some tasks for testing"""
        self.user = User.objects.create_user(phone='09227096188', password='StrongP@ssword1')
        
        # Log in to get the token
        response = self.client.post(reverse('auth:login'), {
            'phone': '09227096188',
            'password': 'StrongP@ssword1'
        }, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # Create some tasks for this user
        self.task1 = Task.objects.create(
            title='Test Task 1',
            description='This is test task 1',
            status='in_progress',
            user=self.user
        )
        self.task2 = Task.objects.create(
            title='Test Task 2',
            description='This is test task 2',
            status='completed',
            user=self.user
        )

        # Define URLs for API endpoints
        self.task_list_url = reverse('tasks-list')
        self.task_detail_url = lambda pk: reverse('task-detail', kwargs={'pk': pk})
        self.new_task_url = reverse('new-tasks')
        self.update_task_url = lambda pk: reverse('update-tasks', kwargs={'pk': pk})
        self.delete_task_url = lambda pk: reverse('delete-tasks', kwargs={'pk': pk})

    def test_list_tasks(self):
        """Test retrieving the list of tasks for authenticated user"""
        response = self.client.get(self.task_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should return two tasks

    def test_retrieve_task(self):
        """Test retrieving a specific task by ID"""
        response = self.client.get(self.task_detail_url(self.task1.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Task 1')

    def test_retrieve_nonexistent_task(self):
        """Test retrieving a task that does not exist"""
        response = self.client.get(self.task_detail_url(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Not found.')

    def test_create_task(self):
        """Test creating a new task"""
        data = {
            'title': 'New Task',
            'description': 'This is a new task',
            'status': 'in_progress'
        }
        response = self.client.post(self.new_task_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Task')

    def test_update_task(self):
        """Test updating an existing task"""
        data = {
            'title': 'Updated Task',
            'description': 'Updated description',
            'status': 'completed'
        }
        response = self.client.put(self.update_task_url(self.task1.pk), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Task')

    def test_update_nonexistent_task(self):
        """Test updating a task that does not exist"""
        data = {
            'title': 'Updated Task',
            'description': 'Updated description',
            'status': 'completed'
        }
        response = self.client.put(self.update_task_url(9999), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Not found.')

    def test_delete_task(self):
        """Test deleting a task"""
        response = self.client.delete(self.delete_task_url(self.task1.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  # Status code should be 204 for successful deletion

    def test_delete_nonexistent_task(self):
        """Test deleting a task that does not exist"""
        response = self.client.delete(self.delete_task_url(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Not found.')
