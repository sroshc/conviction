from django.urls import path, include
from . import views

urlpatterns = [
    path('', include("django.contrib.auth.urls"), name="login"),
    path('create_account', views.CreateAccountView.as_view(), name="create_account"),
    path('view', views.account_view, name="view")
]
