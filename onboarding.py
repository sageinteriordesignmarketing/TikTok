#!/usr/bin/env python3
"""New-client onboarding: GHL proposal paid -> ClickUp + GHL + Slack.

GoHighLevel starts this (through GitHub) when a client pays a proposal. It:
  1. Picks the account manager (AM) with the most free capacity, using their
     open ClickUp work, their active clients and the Time Off Requests list.
  2. Builds the client's ClickUp folder in Agency Clients by copying the
     "Sage Social Studio - Client Template" folder, plus a dated copy of the
     Client Onboarding Timeline, with every task assigned to the AM.
  3. Updates the contact in GHL: assigns the AM, fills in the AM's name,
     email and booking link, and adds the tag that starts the GHL welcome
     email workflow (the email itself is written and sent from GHL).
  4. Posts the new client and the chosen AM to Slack.

Secrets (environment variables, never hard-code them):
  CLICKUP_API_TOKEN   personal ClickUp API token (starts with "pk_")
  GHL_API_TOKEN       GHL Private Integration token (starts with "pit-")
  GHL_LOCATION_ID     the GHL sub-account (location) ID
  SLACK_BOT_TOKEN     Slack bot token (optional; no Slack post without it)
  ONBOARDING_SLACK_CHANNEL_ID   channel for the post (falls back to
                      SLACK_CHANNEL_ID, the overdue-report channel)

Input: the client's details as JSON, from --payload-file or the
CLIENT_PAYLOAD environment variable (GitHub fills it from the GHL webhook):
  {"contact_id": "...", "first_name": "...", "last_name": "...",
   "email": "...", "phone": "...", "company": "...",
   "package": "...", "amount": "...", "account_manager": ""}
Only contact_id and a name (company or first/last) are required.
"account_manager" (an AM's name or email) skips the automatic choice.

Options:
  --dry-run           read everything, change nothing, print the plan
  --payload-file PATH read the client's details from a JSON file

Uses only the Python standard library, so there is nothing to install.
"""

import argparse
import json
import os
import re
import sys
import time as time_mod
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

# --------------------------------------------------------------------------
# Settings. Edit these if your team or workspace changes.
# --------------------------------------------------------------------------
WORKSPACE_ID = "9017037420"
TIMEZONE = ZoneInfo("America/New_York")

AGENCY_CLIENTS_SPACE = "90170894916"        # new client folders go here
CLIENT_TEMPLATE_FOLDER = "90178513273"      # Templates Hub > Sage Social Studio - Client Template
ONBOARDING_TIMELINE_LIST = "901718144560"   # Agency Clients > Client Onboarding Timeline
TIMELINE_LIST_NAME = "Onboarding Timeline"  # name of the dated copy in the client folder
TIME_OFF_LIST = "901702904077"              # Operations > HR > Time Off Requests
TIME_OFF_APPROVED_FIELD = "860894a7-23be-48a4-82fd-da4bbd0c59c3"  # "Approved?" dropdown

# Account managers who can be given new clients.
#   weekly_hours  hours a week they have for client work
#   max_clients   never give them more active clients than this
#   booking_link  their GHL calendar link for the onboarding call (goes in
#                 the welcome email)
# Set "active": False to stop someone getting new clients without deleting them.
ACCOUNT_MANAGERS = [
    {"name": "Bella Gaston", "clickup_id": "95226766",
     "email": "bella@sageinteriordesignmarketing.com",
     "weekly_hours": 30, "max_clients": 6, "booking_link": "", "active": True},
    {"name": "Campbell Fauber", "clickup_id": "89193155",
     "email": "campbell@sageinteriordesignmarketing.com",
     "weekly_hours": 30, "max_clients": 6, "booking_link": "", "active": True},
    {"name": "Hailey Holdahl", "clickup_id": "101382018",
     "email": "hailey@sageinteriordesignmarketing.com",
     "weekly_hours": 30, "max_clients": 6, "booking_link": "", "active": True},
]

# How workload is measured: open tasks assigned to the AM in Agency Clients
# that are overdue or due in the next LOAD_WINDOW_DAYS. A task's time estimate
# is used when it has one, otherwise DEFAULT_TASK_HOURS.
LOAD_WINDOW_DAYS = 14
DEFAULT_TASK_HOURS = 1.0
# Hours a brand-new client adds in their first weeks, used to make sure the
# chosen AM can actually take them on.
NEW_CLIENT_WEEKLY_HOURS = 5
# Someone with approved time off starting within this many days is skipped.
TIME_OFF_LOOKAHEAD_DAYS = 7

# GHL: tag that starts the welcome-email workflow, plus extra tags.
GHL_TRIGGER_TAG = "onboarding - am assigned"
GHL_EXTRA_TAGS = ["client - active"]
# GHL contact custom fields (by name) that the welcome email uses.
GHL_FIELD_AM_NAME = "Account Manager Name"
GHL_FIELD_AM_EMAIL = "Account Manager Email"
GHL_FIELD_AM_BOOKING = "Account Manager Booking Link"

CLICKUP_API = "https://api.clickup.com/api/v2"
GHL_API = "https://services.leadconnectorhq.com"
GHL_VERSION = "2021-07-28"

ALWAYS_OPEN_STATUSES = {"admin"}


# --------------------------------------------------------------------------
# HTTP
# --------------------------------------------------------------------------
class ApiError(Exception):
    pass


def http(method, url, headers, body=None, label="API"):
    data = json.dumps(body).encode() if body is not None else None
    hdrs = {"Accept": "application/json", **headers}
    if data is not None:
        hdrs["Content-Type"] = "application/json"
    for attempt in range(4):
        req = urllib.request.Request(url, data=data, method=method, headers=hdrs)
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                raw = resp.read().decode(errors="replace")
                return json.loads(raw) if raw.strip() else {}
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code >= 500:  # rate limit / hiccup: retry
                time_mod.sleep(2 * (attempt + 1))
                continue
            raise ApiError(f"{label} error {e.code} on {method} {url}: {e.read().decode(errors='replace')}")
    raise ApiError(f"{label} kept failing on {method} {url}")


class ClickUp:
    def __init__(self, token, dry_run):
        self.headers = {"Authorization": token}
        self.dry_run = dry_run
        self._fake = 0

    def get(self, path, params=None):
        url = f"{CLICKUP_API}{path}" + ("?" + urllib.parse.urlencode(params) if params else "")
        return http("GET", url, self.headers, label="ClickUp")

    def post(self, path, body):
        if self.dry_run:
            self._fake += 1
            return {"id": f"dry-run-{self._fake}", "url": "(dry run)"}
        return http("POST", f"{CLICKUP_API}{path}", self.headers, body, label="ClickUp")

    def tasks(self, path, params):
        """All pages of a task listing."""
        out, page = [], 0
        while True:
            data = self.get(path, params + [("page", page)])
            out += data.get("tasks", [])
            if data.get("last_page", True) or not data.get("tasks"):
                return out
            page += 1


class GHL:
    def __init__(self, token, location_id, dry_run):
        self.headers = {"Authorization": f"Bearer {token}", "Version": GHL_VERSION}
        self.location_id = location_id
        self.dry_run = dry_run

    def call(self, method, path, body=None, params=None):
        url = f"{GHL_API}{path}" + ("?" + urllib.parse.urlencode(params) if params else "")
        if self.dry_run and method != "GET":
            return {}
        return http(method, url, self.headers, body, label="GHL")


# --------------------------------------------------------------------------
# 1. Choosing the account manager
# --------------------------------------------------------------------------
def ms(dt):
    return int(dt.timestamp() * 1000)


def is_open(task):
    status = task.get("status") or {}
    if (status.get("status") or "").strip().lower() in ALWAYS_OPEN_STATUSES:
        return True
    return (status.get("type") or "").lower() not in ("closed", "done")


def workload(cu, am, now):
    """(hours of work per week coming up, number of active clients)."""
    tasks = cu.tasks(f"/team/{WORKSPACE_ID}/task", [
        ("assignees[]", am["clickup_id"]),
        ("space_ids[]", AGENCY_CLIENTS_SPACE),
        ("include_closed", "false"),
        ("subtasks", "true"),
        ("archived", "false"),
    ])
    window_end = ms(now + timedelta(days=LOAD_WINDOW_DAYS))
    hours, clients = 0.0, set()
    for t in tasks:
        if not is_open(t):
            continue
        folder = t.get("folder") or {}
        if folder.get("id") and not folder.get("hidden"):
            clients.add(folder["id"])
        if t.get("due_date") and int(t["due_date"]) <= window_end:
            est = t.get("time_estimate")
            hours += int(est) / 3_600_000 if est else DEFAULT_TASK_HOURS
    weekly = hours * 7 / LOAD_WINDOW_DAYS
    return round(weekly, 1), len(clients)


def time_off(cu, now):
    """Names of people with approved time off now or in the next few days."""
    tasks = cu.tasks(f"/list/{TIME_OFF_LIST}/task", [
        ("include_closed", "true"), ("archived", "false")])
    soon = ms(now + timedelta(days=TIME_OFF_LOOKAHEAD_DAYS))
    today = ms(datetime.combine(now.date(), time.min, TIMEZONE))
    away = set()
    for t in tasks:
        end = t.get("due_date")
        start = t.get("start_date") or end
        if not end or int(end) < today or int(start) > soon:
            continue
        approved = next((f for f in t.get("custom_fields") or []
                         if f.get("id") == TIME_OFF_APPROVED_FIELD), {})
        options = (approved.get("type_config") or {}).get("options") or []
        chosen = next((o.get("name", "") for o in options
                       if o.get("id") == approved.get("value") or o.get("orderindex") == approved.get("value")), "")
        if chosen.strip().lower() == "no":
            continue
        away.add((t.get("name") or "").strip().lower())
    return away


def find_am(text):
    text = (text or "").strip().lower()
    if not text:
        return None
    for am in ACCOUNT_MANAGERS:
        if text in (am["name"].lower(), am["email"].lower(), am["name"].split()[0].lower()):
            return am
    sys.exit(f"account_manager '{text}' isn't in ACCOUNT_MANAGERS in onboarding.py.")


def choose_am(cu, now, requested=None):
    """Returns (chosen AM, table of everyone's numbers, note for Slack)."""
    away = time_off(cu, now)
    table = []
    for am in ACCOUNT_MANAGERS:
        if not am.get("active", True):
            continue
        weekly, clients = workload(cu, am, now)
        free = am["weekly_hours"] - weekly
        row = {"am": am, "weekly": weekly, "clients": clients, "free": round(free, 1),
               "away": am["name"].lower() in away, "reason": ""}
        if row["away"]:
            row["reason"] = "time off"
        elif clients >= am["max_clients"]:
            row["reason"] = f"at max clients ({am['max_clients']})"
        elif free < NEW_CLIENT_WEEKLY_HOURS:
            row["reason"] = "not enough free hours"
        table.append(row)
    if not table:
        sys.exit("No active account managers in ACCOUNT_MANAGERS.")
    # Most free hours (as a share of their week) first; fewer clients breaks ties.
    table.sort(key=lambda r: (-(r["free"] / r["am"]["weekly_hours"]), r["clients"]))

    forced = find_am(requested)
    if forced:
        return forced, table, f"chosen by hand ({requested})"
    eligible = [r for r in table if not r["reason"]]
    if eligible:
        return eligible[0]["am"], table, "most free capacity"
    # Everyone is full: still assign, but flag it loudly.
    present = [r for r in table if not r["away"]] or table
    return present[0]["am"], table, "⚠️ everyone is at capacity, so this went to the least-loaded AM"


# --------------------------------------------------------------------------
# 2. Building the ClickUp folder
# --------------------------------------------------------------------------
DAY_RE = re.compile(r"\bDay\s+(\d+)(?:\s*[–—-]\s*(\d+))?", re.I)


def day_offset(*names):
    """'Day 8–14 — Content Build' -> 14. First name with a day wins."""
    for n in names:
        m = DAY_RE.search(n or "")
        if m:
            return int(m.group(2) or m.group(1))
    return None


def copy_list(cu, src_list_id, folder_id, name, assignee, start_day, log):
    tasks = cu.tasks(f"/list/{src_list_id}/task", [
        ("subtasks", "true"), ("include_closed", "true"), ("archived", "false"),
        ("include_markdown_description", "true")])
    new_list = cu.post(f"/folder/{folder_id}/list", {"name": name})
    by_id = {t["id"]: t for t in tasks}
    new_ids, remaining = {}, sorted(tasks, key=lambda t: float(t.get("orderindex") or 0))
    # Parents before their subtasks (handles subtasks of subtasks too).
    while remaining:
        progress, later = False, []
        for t in remaining:
            parent = t.get("parent")
            if parent and parent in by_id and parent not in new_ids:
                later.append(t)
                continue
            parent_name = by_id.get(parent, {}).get("name", "")
            body = {
                "name": t["name"],
                "description": t.get("text_content") or t.get("description") or "",
                "markdown_content": t.get("markdown_description") or t.get("description") or "",
                "assignees": [int(assignee)],
                "tags": [tag["name"] for tag in t.get("tags") or []],
            }
            if t.get("priority"):
                body["priority"] = int(t["priority"]["id"])
            if t.get("time_estimate"):
                body["time_estimate"] = int(t["time_estimate"])
            offset = day_offset(t["name"], parent_name)
            if offset is not None:
                due = datetime.combine(start_day + timedelta(days=offset), time(17), TIMEZONE)
                body["due_date"], body["due_date_time"] = ms(due), False
            if parent in new_ids:
                body["parent"] = new_ids[parent]
            created = cu.post(f"/list/{new_list['id']}/task", body)
            new_ids[t["id"]] = created["id"]
            for checklist in t.get("checklists") or []:
                cl = cu.post(f"/task/{created['id']}/checklist", {"name": checklist["name"]})
                cl_id = (cl.get("checklist") or cl)["id"]
                for item in sorted(checklist.get("items") or [], key=lambda i: i.get("orderindex", 0)):
                    cu.post(f"/checklist/{cl_id}/checklist_item", {"name": item["name"]})
            progress = True
        if not progress:  # parent outside this list: create the rest as top-level
            for t in later:
                t["parent"] = None
        remaining = later
    log.append(f"  list '{name}': {len(tasks)} tasks")
    return new_list


def build_clickup(cu, client_name, am, start_day, log):
    existing = cu.get(f"/space/{AGENCY_CLIENTS_SPACE}/folder", {"archived": "false"}).get("folders", [])
    for f in existing:
        if f["name"].strip().lower() == client_name.strip().lower():
            return f, False  # already onboarded: don't build a second copy
    folder = cu.post(f"/space/{AGENCY_CLIENTS_SPACE}/folder", {"name": client_name})
    template = cu.get(f"/folder/{CLIENT_TEMPLATE_FOLDER}")
    for lst in template.get("lists", []):
        copy_list(cu, lst["id"], folder["id"], lst["name"], am["clickup_id"], start_day, log)
    if ONBOARDING_TIMELINE_LIST:
        copy_list(cu, ONBOARDING_TIMELINE_LIST, folder["id"], TIMELINE_LIST_NAME,
                  am["clickup_id"], start_day, log)
    return folder, True


# --------------------------------------------------------------------------
# 3. GHL
# --------------------------------------------------------------------------
def update_ghl(ghl, client, am, folder_url, log):
    users = ghl.call("GET", "/users/", params={"locationId": ghl.location_id}).get("users", [])
    user = next((u for u in users if (u.get("email") or "").lower() == am["email"].lower()), None)
    if not user:
        log.append(f"  ⚠️ {am['name']} isn't a user in GHL ({am['email']}), so the contact wasn't assigned to them")

    fields = ghl.call("GET", f"/locations/{ghl.location_id}/customFields").get("customFields", [])
    ids = {(f.get("name") or "").strip().lower(): f["id"] for f in fields}
    values = {GHL_FIELD_AM_NAME: am["name"], GHL_FIELD_AM_EMAIL: am["email"],
              GHL_FIELD_AM_BOOKING: am.get("booking_link", "")}
    custom, missing = [], []
    for name, value in values.items():
        if name.lower() in ids:
            custom.append({"id": ids[name.lower()], "field_value": value})
        else:
            missing.append(name)
    if missing:
        log.append("  ⚠️ create these contact fields in GHL: " + ", ".join(missing))

    body = {"customFields": custom}
    if user:
        body["assignedTo"] = user["id"]
    ghl.call("PUT", f"/contacts/{client['contact_id']}", body)
    ghl.call("POST", f"/contacts/{client['contact_id']}/notes", {"body": (
        f"Onboarding started {datetime.now(TIMEZONE):%b %-d, %Y}. "
        f"Account manager: {am['name']}. ClickUp: {folder_url}")})
    # The tag goes last: it starts the welcome email, which needs the fields above.
    ghl.call("POST", f"/contacts/{client['contact_id']}/tags",
             {"tags": GHL_EXTRA_TAGS + [GHL_TRIGGER_TAG]})
    log.append(f"  GHL: assigned, fields filled, tagged '{GHL_TRIGGER_TAG}' (sends the welcome email)")


# --------------------------------------------------------------------------
# 4. Slack
# --------------------------------------------------------------------------
def slack_text(client, client_name, am, why, table, folder_url, log, created):
    who = " ".join(x for x in [client.get("first_name"), client.get("last_name")] if x)
    lines = [f"🎉 *New client paid: {client_name}*" + (f" ({who})" if who and who != client_name else "")]
    if client.get("package") or client.get("amount"):
        lines.append("Package: " + " · ".join(x for x in [client.get("package"), client.get("amount")] if x))
    lines.append(f"*Account manager: {am['name']}* — {why}")
    if created:
        lines.append(f"ClickUp folder: <{folder_url}|{client_name}>  (all tasks assigned to {am['name'].split()[0]})")
    else:
        lines.append(f"ClickUp folder <{folder_url}|{client_name}> already existed, so nothing was copied again.")
    lines.append("\n_Capacity when this was decided (hours/week booked of available · active clients):_")
    for r in table:
        a = r["am"]
        flag = f"  ← {r['reason']}" if r["reason"] else ""
        mark = "👉 " if a is am else "• "
        lines.append(f"{mark}{a['name']}: {r['weekly']}h of {a['weekly_hours']}h · "
                     f"{r['clients']}/{a['max_clients']} clients{flag}")
    warnings = [line.strip() for line in log if "⚠️" in line]
    if warnings:
        lines.append("\n" + "\n".join(warnings))
    return "\n".join(lines)


def post_slack(text):
    token = os.environ.get("SLACK_BOT_TOKEN", "").strip()
    channel = (os.environ.get("ONBOARDING_SLACK_CHANNEL_ID") or os.environ.get("SLACK_CHANNEL_ID") or "").strip()
    if not (token and channel):
        print("No Slack bot token/channel set, so nothing was posted to Slack.")
        return
    data = http("POST", "https://slack.com/api/chat.postMessage", {"Authorization": f"Bearer {token}"},
                {"channel": channel, "text": text, "unfurl_links": False}, label="Slack")
    if not data.get("ok"):
        print(f"Slack error: {data.get('error')} (invite the Slack app to the channel?)")


# --------------------------------------------------------------------------
def load_client(args):
    if args.payload_file:
        with open(args.payload_file) as f:
            raw = json.load(f)
    else:
        raw = json.loads(os.environ.get("CLIENT_PAYLOAD") or "{}")
    client = {k: str(v).strip() for k, v in raw.items() if v is not None}
    # GHL sends "{{contact.company_name}}" etc. unfilled when a field is empty.
    client = {k: ("" if v.startswith("{{") else v) for k, v in client.items()}
    if not client.get("contact_id"):
        sys.exit(f"The webhook didn't include contact_id. Got: {json.dumps(raw)}")
    name = client.get("company") or " ".join(
        x for x in [client.get("first_name"), client.get("last_name")] if x)
    if not name:
        sys.exit("The webhook didn't include a company or first/last name.")
    return client, name


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--payload-file")
    args = ap.parse_args()

    client, client_name = load_client(args)
    cu_token = os.environ.get("CLICKUP_API_TOKEN", "").strip()
    if not cu_token:
        sys.exit("Missing CLICKUP_API_TOKEN secret.")
    cu = ClickUp(cu_token, args.dry_run)
    now = datetime.now(TIMEZONE)
    log = []

    am, table, why = choose_am(cu, now, client.get("account_manager"))
    print(f"Client: {client_name}\nAccount manager: {am['name']} ({why})")

    folder, created = build_clickup(cu, client_name, am, now.date(), log)
    folder_url = f"https://app.clickup.com/{WORKSPACE_ID}/v/f/{folder['id']}"

    ghl_token = os.environ.get("GHL_API_TOKEN", "").strip()
    location = os.environ.get("GHL_LOCATION_ID", "").strip()
    if ghl_token and location:
        try:
            update_ghl(GHL(ghl_token, location, args.dry_run), client, am, folder_url, log)
        except ApiError as e:
            log.append(f"  ⚠️ GHL update failed, so the welcome email did NOT go out: {e}")
    else:
        log.append("  ⚠️ GHL_API_TOKEN / GHL_LOCATION_ID not set: contact not updated, no welcome email")

    text = slack_text(client, client_name, am, why, table, folder_url, log, created)
    print("\n".join(log))
    if args.dry_run:
        print("\n--- DRY RUN: nothing was changed. Slack message would be: ---\n" + text)
        return
    post_slack(text)
    if any("GHL update failed" in line for line in log):
        sys.exit(1)  # the run shows as failed so GitHub emails you


if __name__ == "__main__":
    main()
