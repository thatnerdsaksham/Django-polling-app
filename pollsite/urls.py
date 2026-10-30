"""Project-level URL routes."""
from django.contrib import admin
from django.urls import include, path

from polls import views as polls_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/register/', polls_views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),  # login, logout, password views
    path('', include('polls.urls')),
]
