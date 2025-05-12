from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

from django.http import HttpResponse

# Create your views here.
def account_view(request):
    return HttpResponse("Accounts Page")

class CreateAccountView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/create_account.html"
