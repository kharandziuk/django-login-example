from django.views.generic import TemplateView, View, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.urls import reverse_lazy
from django.http import JsonResponse
import os
from django.core import management
import io


class AboutView(LoginRequiredMixin, TemplateView):
    template_name = "about.html"


class IndexView(TemplateView):
    template_name = "index.html"


class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/sign-up.html"
    success_url = reverse_lazy("login")


def health(request):
    stream = io.StringIO()
    management.call_command("showmigrations", stdout=stream)
    return JsonResponse(
        {
            "db": os.environ["POSTGRES_DB"],
            "status": "ok",
            "migrations": stream.getvalue().split(),
        }
    )
