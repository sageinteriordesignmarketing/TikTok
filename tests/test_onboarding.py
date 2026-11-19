"""Runs onboarding.py end to end against fake ClickUp / GHL / Slack APIs.

    python -m unittest discover tests
"""

import json
import os
import sys
import unittest
from datetime import datetime, timedelta
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import onboarding as ob  # noqa: E402

NOW = datetime(2026, 11, 19, 10, tzinfo=ob.TIMEZONE)
SOON = str(int((NOW + timedelta(days=3)).timestamp() * 1000))


def task(id_, name, assignee=None, folder="f1", due=SOON, est=None, parent=None, **kw):
    return {"id": id_, "name": name, "parent": parent, "orderindex": id_[-1],
            "status": {"status": "to do", "type": "open"}, "due_date": due,
            "time_estimate": est, "folder": {"id": folder, "hidden": False},
            "assignees": [{"id": assignee}] if assignee else [], "tags": [], **kw}


class FakeApis:
    def __init__(self, existing_folders=(), time_off=()):
        self.calls = []
        self.existing = list(existing_folders)
        self.time_off = list(time_off)
        self.n = 0

    def __call__(self, method, url, headers, body=None, label="API"):
        self.calls.append((method, url, body))
        path = url.split("?")[0]
        if method == "GET" and "/team/" in path:
            who = url.split("assignees%5B%5D=")[1].split("&")[0]
            if "page=1" in url:
                return {"tasks": [], "last_page": True}
            if who == "95226766":   # Bella: 20 tasks of 1h due soon, 5 clients
                tasks = [task(f"b{i}", "x", who, folder=f"c{i % 5}") for i in range(20)]
            elif who == "89193155":  # Campbell: light, but on time off
                tasks = [task("c1", "x", who)]
            else:                    # Hailey: 2 tasks of 3h, 2 clients
                tasks = [task("h1", "x", who, est=3 * 3_600_000, folder="a"),
                         task("h2", "x", who, est=3 * 3_600_000, folder="b")]
            return {"tasks": tasks, "last_page": True}
        if method == "GET" and path.endswith(f"/list/{ob.TIME_OFF_LIST}/task"):
            return {"tasks": self.time_off, "last_page": True}
        if method == "GET" and path.endswith("/folder") and "/space/" in path:
            return {"folders": self.existing}
        if method == "GET" and path.endswith(f"/folder/{ob.CLIENT_TEMPLATE_FOLDER}"):
            return {"lists": [{"id": "L1", "name": "Onboarding"}]}
        if method == "GET" and path.endswith("/list/L1/task"):
            return {"tasks": [
                task("t2", "Child", parent="t1", due=None),
                task("t1", "Phase 1 — Account Setup", due=None,
                     checklists=[{"name": "Steps", "items": [{"name": "a", "orderindex": 0}]}]),
            ], "last_page": True}
        if method == "GET" and path.endswith(f"/list/{ob.ONBOARDING_TIMELINE_LIST}/task"):
            return {"tasks": [task("d1", "Day 8–14 — Content Build", due=None),
                              task("d2", "Share with client", due=None, parent="d1")],
                    "last_page": True}
        if method == "GET" and path.endswith("/users/"):
            return {"users": [{"id": "ghl-hailey", "email": "hailey@sageinteriordesignmarketing.com"}]}
        if method == "GET" and "/customFields" in path:
            return {"customFields": [{"id": "cf1", "name": "Account Manager Name"},
                                     {"id": "cf2", "name": "Account Manager Email"},
                                     {"id": "cf3", "name": "Account Manager Booking Link"}]}
        if "slack.com" in url:
            return {"ok": True}
        self.n += 1
        return {"id": f"new{self.n}", "checklist": {"id": f"cl{self.n}"}}


def run(fake, payload, argv=()):
    env = {"CLICKUP_API_TOKEN": "pk_x", "GHL_API_TOKEN": "pit-x", "GHL_LOCATION_ID": "loc",
           "SLACK_BOT_TOKEN": "xoxb", "SLACK_CHANNEL_ID": "C1", "CLIENT_PAYLOAD": json.dumps(payload)}
    fixed = mock.Mock(wraps=datetime)
    fixed.now.return_value = NOW
    with mock.patch.dict(os.environ, env), mock.patch.object(ob, "http", fake), \
            mock.patch.object(ob, "datetime", fixed), \
            mock.patch.object(sys, "argv", ["onboarding.py", *argv]), \
            mock.patch("builtins.print"):
        ob.main()
    return fake.calls


PAYLOAD = {"contact_id": "abc", "first_name": "Jane", "last_name": "Doe",
           "company": "Doe Interiors", "package": "{{payment.product}}"}
TIME_OFF = [{"name": "Campbell Fauber", "due_date": SOON, "start_date": None, "custom_fields": []}]


class OnboardingTest(unittest.TestCase):
    def test_full_run(self):
        calls = run(FakeApis(time_off=TIME_OFF), PAYLOAD)
        posts = [(u, b) for m, u, b in calls if m in ("POST", "PUT")]
        # Bella has 10h/week booked + 5 clients; Campbell is off -> Hailey (3h/week).
        folder = next(b for u, b in posts if u.endswith(f"/space/{ob.AGENCY_CLIENTS_SPACE}/folder"))
        self.assertEqual(folder["name"], "Doe Interiors")
        new_tasks = [b for u, b in posts if u.endswith("/task") and "/list/" in u]
        self.assertEqual(len(new_tasks), 4)
        self.assertTrue(all(b["assignees"] == [101382018] for b in new_tasks))
        # Parent created before child, and the child points at it.
        names = [b["name"] for b in new_tasks]
        self.assertLess(names.index("Phase 1 — Account Setup"), names.index("Child"))
        self.assertIn("parent", new_tasks[names.index("Child")])
        # "Day 8–14" -> due 14 days out, and its subtask inherits that.
        day = next(b for b in new_tasks if b["name"].startswith("Day"))
        sub = next(b for b in new_tasks if b["name"] == "Share with client")
        self.assertEqual(datetime.fromtimestamp(day["due_date"] / 1000, ob.TIMEZONE).date(),
                         (NOW + timedelta(days=14)).date())
        self.assertEqual(sub["due_date"], day["due_date"])
        self.assertTrue(any(u.endswith("/checklist_item") for u, _ in posts))
        # GHL: assigned to Hailey's GHL user, fields filled, tag added last.
        put = next(b for u, b in posts if "/contacts/abc" in u and "notes" not in u and "tags" not in u)
        self.assertEqual(put["assignedTo"], "ghl-hailey")
        self.assertEqual(put["customFields"][0], {"id": "cf1", "field_value": "Hailey Holdahl"})
        ghl_urls = [u for u, _ in posts if "leadconnector" in u]
        self.assertTrue(ghl_urls[-1].endswith("/contacts/abc/tags"))
        slack = next(b for u, b in posts if "slack.com" in u)["text"]
        self.assertIn("Account manager: Hailey Holdahl", slack)
        self.assertIn("time off", slack)
        self.assertNotIn("{{", slack)  # unfilled GHL merge field was dropped

    def test_dry_run_changes_nothing(self):
        calls = run(FakeApis(), PAYLOAD, ["--dry-run"])
        self.assertEqual([c for c in calls if c[0] != "GET"], [])

    def test_existing_folder_is_not_copied_again(self):
        calls = run(FakeApis(existing_folders=[{"id": "F9", "name": "doe interiors"}]), PAYLOAD)
        self.assertFalse(any(m == "POST" and "clickup" in u for m, u, _ in calls))

    def test_forced_am(self):
        calls = run(FakeApis(), {**PAYLOAD, "account_manager": "bella"})
        task_body = next(b for m, u, b in calls if m == "POST" and u.endswith("/task"))
        self.assertEqual(task_body["assignees"], [95226766])


if __name__ == "__main__":
    unittest.main()
