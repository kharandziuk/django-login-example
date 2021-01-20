from django.views.generic import TemplateView, View, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.urls import reverse_lazy
from django.http import JsonResponse
import os
from django.core import management
import io

from core import models


class AboutView(LoginRequiredMixin, ListView):
    template_name = "about.html"
    model = models.Item

    def get_queryset(self):
        return self.request.user.items.all()


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
            "migrations": stream.getvalue().split("\n"),
        }
    )
