from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from accounts import views as account_views
from tourism import views as tourism_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')), 
    path('accounts/', include('django.contrib.auth.urls')), 
    
    # PWA Core Routes
    path('service-worker.js', TemplateView.as_view(template_name="service-worker.js", content_type='application/javascript'), name='service-worker'),
    path('offline/', TemplateView.as_view(template_name="offline.html"), name='offline_fallback'),
    
    # App Routes
    path('', account_views.home, name='home'), 
    path('report/<int:pk>/comment/', account_views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', account_views.delete_comment, name='delete_comment'),
    path('like/<int:pk>/', account_views.toggle_like, name='toggle_like'), 
    path('analytics/', tourism_views.analytics_dashboard, name='analytics_dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)