"""Shared helpers for the Dawra Campus tests. Every test starts from the synthetic demo data."""

import os
import re
from datetime import date, timedelta
from io import StringIO
from types import SimpleNamespace
from unittest import mock

from django.core.management import call_command
from django.test import TestCase

from accounts.models import User

PASSWORD = "dawra-demo-2026"


class DemoTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # The test users always get the local demo password, even where DEMO_PASSWORD is set (for example online).
        with mock.patch.dict(os.environ, {"DEMO_PASSWORD": PASSWORD}):
            call_command("seed_demo", stdout=StringIO())

    def sign_in(self, username, role=None):
        client = self.client_class()
        response = client.post("/accounts/sign-in/", {"username": username, "password": PASSWORD})
        self.assertEqual(response.status_code, 302, f"{username} could not sign in")
        if role:
            user_role = User.objects.get(username=username).user_roles.get(role__code=role)
            client.post("/accounts/switch-role/", {"user_role": user_role.pk})
        return client

    @staticmethod
    def errors(response):
        return re.findall(r'class="toast error"><svg[^>]*>.*?</svg><span>(.*?)</span>', response.content.decode())

    @staticmethod
    def future(days=10):
        return (date.today() + timedelta(days=days)).isoformat()


class FakeClaude:
    """Stands in for the Anthropic client so the AI tests run without a key or network.
    answers maps an output class to a function(prompt text) returning an instance of it."""

    def __init__(self, answers):
        self.answers = answers
        self.messages = self
        self.calls = 0

    def with_options(self, **kwargs):
        return self

    def parse(self, model, max_tokens, system, messages, output_format, output_config=None):
        self.calls += 1
        self.output_format, self.output_config = output_format, output_config
        # The classification structure is built per request, so match it by its base class.
        answer = next(f for kind, f in self.answers.items() if issubclass(output_format, kind))(messages[0]["content"])
        return SimpleNamespace(stop_reason="end_turn", parsed_output=answer)
