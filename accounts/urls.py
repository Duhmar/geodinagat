from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Profile & Authentication
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/password/', views.change_password, name='change_password'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    # Reports Management
    path('reports/', views.report_list, name='report_list'),
    path('reports/new/', views.report_create, name='report_create'),
    path('reports/<int:pk>/edit/', views.report_update, name='report_update'),
    path('reports/<int:pk>/delete/', views.report_delete, name='report_delete'),
    path('admin-delete/<int:pk>/', views.admin_delete_report, name='admin_delete'),
]