import json

from django.test import TestCase

from desk.auth_utils import create_access_token
from desk.models import OffsetSubmission, User
from desk.services import evaluate_verdict


class RoleTests(TestCase):
    def test_can_write_by_role(self):
        self.assertTrue(User(role=User.Role.MACHINIST).can_write)
        self.assertFalse(User(role=User.Role.AUDITOR).can_write)


class SubmissionAuthzTests(TestCase):
    def setUp(self):
        self.machinist = User.objects.create(username="m1", role=User.Role.MACHINIST)
        self.auditor = User.objects.create(username="a1", role=User.Role.AUDITOR)

    def post(self, user=None):
        headers = {}
        if user is not None:
            headers["HTTP_AUTHORIZATION"] = f"Bearer {create_access_token(user)}"
        return self.client.post(
            "/api/submissions",
            data=json.dumps({"tool_code": "T77", "offset_um": 1}),
            content_type="application/json",
            **headers,
        )

    def test_auditor_post_rejected_and_not_persisted(self):
        before = OffsetSubmission.objects.count()
        resp = self.post(self.auditor)
        self.assertEqual(resp.status_code, 403)
        # 复核员被拒收，数据库不得多出一行
        self.assertEqual(OffsetSubmission.objects.count(), before)
        self.assertFalse(OffsetSubmission.objects.filter(tool_code="T77").exists())

    def test_machinist_post_accepted(self):
        resp = self.post(self.machinist)
        self.assertEqual(resp.status_code, 200)
        row = OffsetSubmission.objects.get(tool_code="T77")
        self.assertEqual(row.status, OffsetSubmission.Status.PENDING)
        self.assertEqual(row.submitted_by, self.machinist)
        self.assertEqual(row.verdict, "")

    def test_unauthenticated_post_rejected(self):
        resp = self.post()
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(OffsetSubmission.objects.count(), 0)


class VerdictBoundaryTests(TestCase):
    def test_seeds_and_tolerance_boundary(self):
        cases = {
            5: OffsetSubmission.Verdict.PASS,    # 甲刀种子仍合格
            20: OffsetSubmission.Verdict.FAIL,   # 乙刀种子仍超差
            12: OffsetSubmission.Verdict.PASS,   # 压线 ±12 微米判合格
            -12: OffsetSubmission.Verdict.PASS,
            13: OffsetSubmission.Verdict.FAIL,
            -13: OffsetSubmission.Verdict.FAIL,
        }
        for offset_um, expected in cases.items():
            with self.subTest(offset_um=offset_um):
                self.assertEqual(evaluate_verdict(offset_um), expected)
