from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

from django.core.exceptions import ValidationError

class Task(models.Model):

    STATUS_CHOICES = (
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='in_progress',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(status__in=['in_progress', 'completed']),
                name='status_valid_choice'
            )
        ]

    def __str__(self):
        return self.title

