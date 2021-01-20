from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from core import models


class ItemListView(LoginRequiredMixin, ListView):
    template_name = "items/list.html"
    model = models.Item

    def get_queryset(self):
        return self.request.user.items.all()


class ItemCreateView(CreateView):
    template_name = "items/create.html"
    model = models.Item
    success_url = reverse_lazy("core:item-list")
    fields = ("name", "owner")
