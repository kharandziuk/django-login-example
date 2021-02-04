from django.urls import reverse

import pytest


pytestmark = pytest.mark.django_db


def test_create_user_and_set_password(client):
    response = client.get(reverse("index"), follow=True)
    assert response.status_code == 200
