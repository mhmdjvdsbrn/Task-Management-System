from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter,OpenApiResponse
from drf_spectacular.types import OpenApiTypes

from task_backend.projects.models import Task
from task_backend.projects.general_serializer import TaskSelectorsSerializer, TaskServicesSerializer
from task_backend.projects.selectors import list_tasks, get_task
from task_backend.projects.services import new_task, update_task, delete_task
from django.utils.dateparse import parse_datetime



@extend_schema(
    request=None,  # No request body for the list action
    responses={200: TaskSelectorsSerializer, 400: TaskSelectorsSerializer, 404: None},
    operation_id='Selectors Tasks',
    parameters=[
        OpenApiParameter(
            name='title',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Filter tasks by title (case-insensitive substring match)',
            required=False,
        ),
        OpenApiParameter(
            name='created_at',
            type=OpenApiTypes.DATETIME,
            location=OpenApiParameter.QUERY,
            description='Filter tasks by creation date (ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ)',
            required=False,
        ),
    ]
)
class TaskViewSelector(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        Retrieve a list of tasks for the authenticated user with optional filtering by title and created_at.
        """
        title = request.query_params.get('title', None)
        created_at = request.query_params.get('created_at', None)

        # Get all tasks for the authenticated user
        list_task = list_tasks(user_id=request.user)

        # Apply filtering based on title and created_at
        if title:
            list_task = list_task.filter(title__icontains=title)

        if created_at:
            try:
                parsed_date = parse_datetime(created_at)
                if parsed_date:
                    list_task = list_task.filter(created_at__date=parsed_date.date())
            except ValueError:
                return Response({'detail': 'Invalid date format. Please use ISO 8601 format.'}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize and return the filtered tasks
        serializer = TaskSelectorsSerializer(list_task, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Retrieve a single task by its ID for the authenticated user.
        """
        try:
            task = get_task(pk=pk, user_id=request.user)
        except Task.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSelectorsSerializer(task)
        return Response(serializer.data)

@extend_schema(
    request=TaskServicesSerializer,
    responses={
        200: TaskSelectorsSerializer,
        400: OpenApiResponse(description="Task creation failed"),
    },
    description="Create a new task for the authenticated user."
)
class TaskViewServices(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        """
        Create a new task for the authenticated user.
        """
        serializer = TaskServicesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            task = new_task(
                user_id=request.user,
                title=serializer.validated_data.get("title"),
                description=serializer.validated_data.get("description"),
                status=serializer.validated_data.get("status"),
            )
            return Response(TaskSelectorsSerializer(task).data, status=status.HTTP_201_CREATED)  # Change to 201 Created
        except Exception as ex:
            return Response({"error": f"Task creation failed. Error: {ex}"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """
        Update an existing task for the authenticated user.
        """
        serializer = TaskServicesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            task = update_task(
                pk=pk,
                user_id=request.user,
                title=serializer.validated_data.get("title"),
                description=serializer.validated_data.get("description"),
                status=serializer.validated_data.get("status"),
            )
            return Response(TaskSelectorsSerializer(task).data)
        except Task.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)  # Ensure 404 for not found
        except Exception as ex:
            return Response({"error": f"Task update failed. Error: {ex}"}, status=status.HTTP_400_BAD_REQUEST)

                            
    def destroy(self, request, pk=None):
        """
        Delete a task for the authenticated user.
        """
        try:
            task = delete_task(
                pk=pk,
                user_id=request.user,
            )
            return Response({'detail': 'Deleted Task.'}, status=status.HTTP_204_NO_CONTENT)  # Change to 204 No Content
        except Task.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
