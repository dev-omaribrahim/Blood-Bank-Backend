from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import Test, LogoutView


urlpatterns = [
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('test/', Test.as_view(), name="test"),
    path('logout/', LogoutView.as_view(), name="logout"),
]