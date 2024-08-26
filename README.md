Here's the updated README document with the detailed API Endpoints:

---

# Task Management BackEnd

This project is a simple Task Management System built with Django and Django REST Framework. It allows users to manage their tasks efficiently, with custom authentication using mobile phone numbers and passwords.


## Project Setup

1. **Navigate to the project directory:**
   ```bash
   cd Task_Management
   ```

2. **Set up a virtual environment:**
   ```bash
   virtualenv -p python3.10 venv
   source venv/bin/activate
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create your environment file:**
   ```bash
   cp .env.dev .env
   ```

5. **Create database tables:**
   ```bash
   python manage.py migrate
   ```

6. **Spin up Docker Compose:**
   ```bash
   docker compose -f compose.yml up -d
   ```

7. **Run the project:**
   ```bash
   python manage.py runserver
   ```

## Testing the models,validators,selectors,serveices & API View

1. **Running Unit Tests:**
   - To run the unit tests for your project, execute the following command:
     ```bash
     python manage.py test
     ```

2. **API Endpoints:**
   - The API can be accessed via the following endpoints:
     - `/api/auth/jwt/login/` - User login.
     - `/api/auth/jwt/refresh/` - Refresh token.
     - `/api/auth/jwt/logout/` - User logout.
     - `/api/users/register/` - Register a new user.
     - `/api/users/profile/` - View user profile.
     - `/api/users/profile/verify/` - Complete profile verification.
     - `/api/tasks-list/` - List tasks.
     - `/api/tasks-detail/<int:pk>/` - Retrieve task details.
     - `/api/new_tasks/` - Create a new task.
     - `/api/update_tasks/<int:pk>/` - Update a task.
     - `/api/delete_tasks/<int:pk>/` - Delete a task.

   - Explore the full API documentation via the Swagger UI at `/api/schema/swagger-ui/`.

### Filtering Tasks

- You can filter tasks by `title` and `created_at` by passing the relevant query parameters to the task list endpoint. For example:
  ```bash
  /tasks-list/?title=shopping
  /tasks-list/?created_at=2024-08-26
  ```

### Example User

To test the API, you can use the following example user credentials:

```json
{
  "phone": "09227096188",
  "password": "Strong@123"
}
```




