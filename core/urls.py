from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'institutes', views.InstituteViewSet)
router.register(r'roles', views.RoleViewSet)
router.register(r'students', views.StudentViewSet)
router.register(r'faculty', views.FacultyViewSet)

urlpatterns = [
    path('auth/register/', views.register, name='auth_register'),
    path('auth/login/', views.login, name='auth_login'),
    path('auth/logout/', views.logout, name='auth_logout'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/profile/', views.profile, name='auth_profile'),
    path('', include(router.urls)),
]