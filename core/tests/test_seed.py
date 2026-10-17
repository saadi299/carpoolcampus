import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError


@pytest.mark.django_db
def test_seed_creates_admin_once(settings):
    settings.DEBUG = True
    call_command("seed")
    call_command("seed")  # second run must not fail or duplicate
    assert get_user_model().objects.filter(username="admin").count() == 1


@pytest.mark.django_db
def test_seed_refuses_without_debug(settings):
    settings.DEBUG = False
    with pytest.raises(CommandError):
        call_command("seed")
