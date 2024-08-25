from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .apis import JWTLoginView, JWTLogoutView
app_name = 'auth'  # Namespace for authentication URLs

urlpatterns = [
        path('jwt/', include(([
            # path('login/', TokenObtainPairView.as_view(),name="login"),
            path('login/', JWTLoginView.as_view(),name="login"),
            path('refresh/', TokenRefreshView.as_view(),name="refresh"),
            path('logout/', JWTLogoutView.as_view(),name="logout"),
            ])), name="jwt"),
]
