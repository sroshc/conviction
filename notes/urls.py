from django.urls import path
from . import views

urlpatterns = [
    path('file/<path:directory>/', views.notes_view, name="notes")
]