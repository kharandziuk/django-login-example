import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        try:
            root = User.objects.create_superuser(
                settings.DEFAULT_ROOT_USER,
                "admin@example.com",
                settings.DEFAULT_ROOT_PASS,
            )
        except IntegrityError:
            pass
