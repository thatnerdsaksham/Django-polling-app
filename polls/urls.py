"""App-level URL routes; included from pollsite/urls.py."""
from django.urls import path

from . import views

app_name = 'polls'  # namespace, so templates use {% url 'polls:detail' id %}

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
]
