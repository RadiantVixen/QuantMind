from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import AnalysisRun

User = get_user_model()

STRONG_PASSWORD = "c0rrect-Horse-battery"


class AuthTests(APITestCase):
    def setUp(self):
        cache.clear()  # reset login/register throttling between tests

    def test_register_returns_token(self):
        res = self.client.post(
            "/api/auth/register/",
            {"username": "alice", "password": STRONG_PASSWORD},
            format="json",
        )
        self.assertEqual(res.status_code, 201)
        self.assertIn("token", res.data)
        self.assertEqual(res.data["user"]["username"], "alice")

    def test_register_rejects_weak_password(self):
        res = self.client.post(
            "/api/auth/register/",
            {"username": "alice", "password": "123"},
            format="json",
        )
        self.assertEqual(res.status_code, 400)
        self.assertFalse(User.objects.filter(username="alice").exists())

    def test_register_rejects_duplicate_username(self):
        User.objects.create_user("alice", password=STRONG_PASSWORD)
        res = self.client.post(
            "/api/auth/register/",
            {"username": "ALICE", "password": STRONG_PASSWORD},
            format="json",
        )
        self.assertEqual(res.status_code, 400)

    def test_login_and_me(self):
        User.objects.create_user("alice", password=STRONG_PASSWORD)
        res = self.client.post(
            "/api/auth/login/",
            {"username": "alice", "password": STRONG_PASSWORD},
            format="json",
        )
        self.assertEqual(res.status_code, 200)

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {res.data['token']}")
        me = self.client.get("/api/auth/me/")
        self.assertEqual(me.status_code, 200)
        self.assertEqual(me.data["username"], "alice")

    def test_login_wrong_password(self):
        User.objects.create_user("alice", password=STRONG_PASSWORD)
        res = self.client.post(
            "/api/auth/login/",
            {"username": "alice", "password": "wrong"},
            format="json",
        )
        self.assertEqual(res.status_code, 400)

    def test_logout_invalidates_token(self):
        user = User.objects.create_user("alice", password=STRONG_PASSWORD)
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        self.assertEqual(self.client.post("/api/auth/logout/").status_code, 204)
        self.assertEqual(self.client.get("/api/auth/me/").status_code, 401)

    def test_protected_endpoints_require_token(self):
        self.assertEqual(self.client.post("/api/analysis/", {}).status_code, 401)
        self.assertEqual(self.client.post("/api/approval/", {}).status_code, 401)
        self.assertEqual(self.client.get("/api/market-data/").status_code, 401)
        self.assertEqual(self.client.get("/api/auth/me/").status_code, 401)


FAKE_ANALYSIS = {
    "thread_id": "thread-1",
    "decision": "BUY",
    "approval_required": True,
}


class ApprovalOwnershipTests(APITestCase):
    def setUp(self):
        self.alice = User.objects.create_user("alice", password=STRONG_PASSWORD)
        self.bob = User.objects.create_user("bob", password=STRONG_PASSWORD)

    def login(self, user):
        token, _ = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    @patch("api.views.run_analysis", return_value=FAKE_ANALYSIS)
    def test_analysis_records_owner(self, _):
        self.login(self.alice)
        res = self.client.post("/api/analysis/", {}, format="json")
        self.assertEqual(res.status_code, 200)

        run = AnalysisRun.objects.get(thread_id="thread-1")
        self.assertEqual(run.user, self.alice)
        self.assertEqual(run.approval_status, "PENDING")

    @patch("api.views.resume_analysis")
    def test_other_user_cannot_approve(self, resume):
        AnalysisRun.objects.create(
            user=self.alice, thread_id="thread-1", symbol="BTC/USDT", timeframe="1h"
        )
        self.login(self.bob)
        res = self.client.post(
            "/api/approval/", {"thread_id": "thread-1", "approved": True}, format="json"
        )
        self.assertEqual(res.status_code, 404)
        resume.assert_not_called()

    @patch(
        "api.views.resume_analysis",
        return_value={"thread_id": "thread-1", "approval_status": "APPROVED"},
    )
    def test_owner_can_approve_once(self, resume):
        AnalysisRun.objects.create(
            user=self.alice, thread_id="thread-1", symbol="BTC/USDT", timeframe="1h"
        )
        self.login(self.alice)
        body = {"thread_id": "thread-1", "approved": True}

        first = self.client.post("/api/approval/", body, format="json")
        self.assertEqual(first.status_code, 200)
        self.assertEqual(
            AnalysisRun.objects.get(thread_id="thread-1").approval_status, "APPROVED"
        )

        second = self.client.post("/api/approval/", body, format="json")
        self.assertEqual(second.status_code, 409)
        resume.assert_called_once()
