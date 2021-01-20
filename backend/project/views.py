from django.views.generic import TemplateView, View, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.urls import reverse_lazy


class AboutView(LoginRequiredMixin, TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        from IPython.core import debugger

        debugger.Pdb().set_trace()
        return context


class IndexView(TemplateView):
    template_name = "index.html"


class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/sign-up.html"
    success_url = reverse_lazy("login")
