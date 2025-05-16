from django.urls import path
from . import views

urlpatterns = [
    path('root/<path:directory>/', views.notes_view, name="notes_view"),
    path('root/', views.root_view, name="root")
]