#!/usr/bin/env python3
"""Daily overdue-task report: ClickUp -> Slack.

Reads two secrets from environment variables (never hard-code them):
  CLICKUP_API_TOKEN   personal ClickUp API token (starts with "pk_")
  SLACK_BOT_TOKEN     Slack bot token (starts with "xoxb-") - lets the full
  SLACK_CHANNEL_ID    lists go in a thread under the report
  SLACK_WEBHOOK_URL   Slack incoming-webhook URL - fallback if the two above
                      aren't set (no thread replies then)

Options:
  --dry-run           print the Slack message instead of posting it
  --from-file PATH    read tasks from a JSON file instead of calling ClickUp
                      (used for previews/tests; same shape as the ClickUp API)

Uses only the Python standard library, so there is nothing to install.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, time
from zoneinfo import ZoneInfo

# --------------------------------------------------------------------------
# Settings. Edit these if your workspace changes.
# --------------------------------------------------------------------------
WORKSPACE_ID = "9017037420"
TIMEZONE = ZoneInfo("America/New_York")

AGENCY_CLIENTS_SPACE = "90170894916"
INCLUDED_SPACES = [
    AGENCY_CLIENTS_SPACE,  # Agency Clients (one folder per client)
    "90170894915",         # Operations
    "90170894914",         # Growth
]
EXCLUDED_SPACES = {"90172978077"}  # Templates Hub: placeholder tasks, never report

# Team roster, in the order people appear in the report.
TEAM = {
    "95226766": "Bella Gaston",
    "89193155": "Campbell Fauber",
    "101382018": "Hailey Holdahl",
    "50294819": "Kyra Clark",
}

CLIENT_DEADLINE_PREFIX = "CLIENT DEADLINE"

# Statuses that always count as open (not finished), even if a list in ClickUp
# has them set up as a "done" status.
ALWAYS_OPEN_STATUSES = {"admin"}

# Show at most this many tasks per person / section; the rest are summarised
# as "+N more". Tasks are sorted most-overdue first, so the oldest always show.
MAX_LINES_PER_SECTION = 12

API = "https://api.clickup.com/api/v2"


# --------------------------------------------------------------------------
# ClickUp
# --------------------------------------------------------------------------
def fetch_overdue_tasks(token, before_ms):
    """All open, unarchived tasks in the included spaces due before `before_ms`."""
    tasks, page = [], 0
    while True:
        params = [
            ("page", page),
            ("due_date_lt", before_ms),
            ("include_closed", "false"),
            ("archived", "false"),
            ("subtasks", "true"),
            ("order_by", "due_date"),
            ("reverse", "true"),
        ] + [("space_ids[]", s) for s in INCLUDED_SPACES]
        url = f"{API}/team/{WORKSPACE_ID}/task?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"Authorization": token})
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.load(resp)
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors="replace")
            hint = " (check the CLICKUP_API_TOKEN secret)" if e.code in (401, 403) else ""
            sys.exit(f"ClickUp API error {e.code}{hint}: {body}")
        tasks.extend(data.get("tasks", []))
        if data.get("last_page", True) or not data.get("tasks"):
            return tasks
        page += 1


# --------------------------------------------------------------------------
# Shaping the data
# --------------------------------------------------------------------------
def today_local():
    return datetime.now(TIMEZONE).date()


def start_of_day_ms(day):
    return int(datetime.combine(day, time.min, TIMEZONE).timestamp() * 1000)


def client_name(task):
    """Client = folder name in Agency Clients; otherwise the space/folder name."""
    space_id = str((task.get("space") or {}).get("id", ""))
    folder = task.get("folder") or {}
    folder_name = None if folder.get("hidden") else folder.get("name")
    if space_id == AGENCY_CLIENTS_SPACE:
        return folder_name or "Agency (general)"
    space_label = {"90170894915": "Operations", "90170894914": "Growth"}.get(space_id, "Other")
    return f"{space_label} / {folder_name}" if folder_name else space_label


def is_open(task):
    if task.get("archived"):
        return False
    status = task.get("status") or {}
    if (status.get("status") or "").strip().lower() in ALWAYS_OPEN_STATUSES:
        return True
    return (status.get("type") or "").lower() not in ("closed", "done")


def build_items(tasks, today):
    items = []
    for t in tasks:
        if str((t.get("space") or {}).get("id")) in EXCLUDED_SPACES:
            continue
        if str((t.get("space") or {}).get("id")) not in INCLUDED_SPACES:
            continue
        if not t.get("due_date") or not is_open(t):
            continue
        due = datetime.fromtimestamp(int(t["due_date"]) / 1000, TIMEZONE).date()
        days = (today - due).days
        if days < 1:
            continue  # due today or later: not overdue yet
        name = (t.get("name") or "").strip()
        is_deadline = name.upper().startswith(CLIENT_DEADLINE_PREFIX)
        if is_deadline:
            # "CLIENT DEADLINE | February footage" -> "February footage"
            name = name[len(CLIENT_DEADLINE_PREFIX):].lstrip(" |:-–—").strip() or name
        items.append({
            "id": t["id"],
            "name": name,
            "url": t.get("url") or f"https://app.clickup.com/t/{t['id']}",
            "client": client_name(t),
            "days": days,
            "assignees": [
                (str(a["id"]), TEAM.get(str(a["id"])) or a.get("username") or "Unknown")
                for a in (t.get("assignees") or [])
            ],
            "deadline": is_deadline,
        })
    items.sort(key=lambda i: (-i["days"], i["client"], i["name"]))
    return items


# --------------------------------------------------------------------------
# Slack message
# --------------------------------------------------------------------------
def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def link(item):
    name = item["name"] if len(item["name"]) <= 90 else item["name"][:87] + "…"
    return f"<{item['url']}|{esc(name)}>"


def days_label(n):
    return f"{n}d"


def plural(n, word):
    return f"{n} {word}{'' if n == 1 else 's'}"


def client_lines(items):
    """Lines grouped under client sub-headings (items already most-overdue first)."""
    groups = defaultdict(list)
    for i in items:
        groups[i["client"]].append(i)
    out = []
    for client, group in groups.items():
        out.append(f"_{esc(client)}_")
        out += [f"   • {link(i)}  ·  *{days_label(i['days'])}*" for i in group]
    return out


def section(text):
    """A Slack section block (max 3000 chars, so long text is split)."""
    blocks, chunk = [], ""
    for line in text.split("\n"):
        if len(chunk) + len(line) + 1 > 2900:
            blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": chunk}})
            chunk = ""
        chunk += line + "\n"
    if chunk.strip():
        blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": chunk}})
    return blocks


def build_message(items, today, threads=False):
    """Returns (main message, list of thread replies with the full lists).

    With threads=False (webhook only, which can't reply in threads) the
    replies are empty and cut-off lists just say "+N more".
    """
    replies = []

    def capped(head, tasks, full_title):
        lines = [head] + client_lines(tasks[:MAX_LINES_PER_SECTION])
        hidden = len(tasks) - MAX_LINES_PER_SECTION
        if hidden > 0:
            if threads:
                lines.append(f"   _+{hidden} more, all less overdue — full list in the thread 🧵_")
                replies.append(reply_message(f"{full_title} ({len(tasks)})", client_lines(tasks)))
            else:
                lines.append(f"   _+{hidden} more, all less overdue_")
        return section("\n".join(lines))

    team_tasks = [i for i in items if not i["deadline"]]
    deadlines = [i for i in items if i["deadline"]]
    unassigned = [i for i in team_tasks if not i["assignees"]]
    date_str = today.strftime("%a %b %-d")

    if not items:
        text = f"✅ *All clear for {date_str}* — no overdue team tasks or client deadlines. Nice work!"
        return {"text": text, "blocks": section(text)}, []

    summary = (
        f"*{plural(len(team_tasks), 'overdue team task')}*"
        + (f" ({len(unassigned)} unassigned)" if unassigned else "")
        + f"  ·  *{plural(len(deadlines), 'overdue client deadline')}*"
    )
    blocks = [
        {"type": "header", "text": {"type": "plain_text", "text": f"Overdue report · {date_str}"}},
        {"type": "section", "text": {"type": "mrkdwn", "text": summary}},
    ]

    # 1. Team tasks by person, then by client.
    by_person = defaultdict(list)
    for i in team_tasks:
        for person_id, _ in i["assignees"]:
            by_person[person_id].append(i)
    names = {pid: name for i in team_tasks for pid, name in i["assignees"]}
    order = [pid for pid in TEAM if by_person.get(pid)] + sorted(
        (pid for pid in by_person if pid not in TEAM), key=lambda p: names[p])
    if order:
        blocks.append({"type": "divider"})
        blocks += section("*👤 TEAM TASKS*")
        for pid in order:
            tasks = by_person[pid]
            label = TEAM.get(pid) or f"{names[pid]} (not on roster)"
            head = f"*{esc(label)}*  —  {len(tasks)} overdue, oldest {days_label(tasks[0]['days'])}"
            blocks += capped(head, tasks, f"*{esc(label)}* — all overdue tasks")
    caught_up = [name for pid, name in TEAM.items() if not by_person.get(pid)]
    if caught_up:
        blocks.append({"type": "context", "elements": [
            {"type": "mrkdwn", "text": "✅ Caught up: " + ", ".join(caught_up)}]})

    # 2. Unassigned.
    if unassigned:
        blocks.append({"type": "divider"})
        head = f"*⚠️ UNASSIGNED — needs an owner* ({len(unassigned)})"
        blocks += capped(head, unassigned, "*⚠️ Unassigned* — all overdue tasks")

    # 3. Client deadlines.
    if deadlines:
        blocks.append({"type": "divider"})
        lines = [f"*📥 CLIENT DEADLINES — waiting on clients* ({len(deadlines)})"]
        for i in deadlines[:MAX_LINES_PER_SECTION * 2]:
            owner = ", ".join(n for _, n in i["assignees"]) or "⚠️ no owner"
            lines.append(f"• *{esc(i['client'])}* — {link(i)}  ·  *{days_label(i['days'])}*  ·  follow-up: {esc(owner)}")
        if len(deadlines) > MAX_LINES_PER_SECTION * 2:
            lines.append(f"_+{len(deadlines) - MAX_LINES_PER_SECTION * 2} more_")
        blocks += section("\n".join(lines))

    blocks.append({"type": "context", "elements": [{"type": "mrkdwn", "text":
        "Overdue = due before today (ET). Most overdue first. Templates Hub, closed and archived tasks excluded."}]})

    if len(blocks) > 50:  # Slack's hard limit per message
        blocks = blocks[:49] + [{"type": "context", "elements": [
            {"type": "mrkdwn", "text": "_Message trimmed — open ClickUp for the full list._"}]}]
    return {"text": f"Overdue report {date_str}: {summary.replace('*', '')}", "blocks": blocks}, replies


def reply_message(title, lines):
    blocks = section("\n".join([title] + lines))
    if len(blocks) > 50:
        blocks = blocks[:49] + [{"type": "context", "elements": [
            {"type": "mrkdwn", "text": "_List trimmed — open ClickUp for the rest._"}]}]
    return {"text": title.replace("*", ""), "blocks": blocks}


def http_post_json(url, payload, headers=None):
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json; charset=utf-8", **(headers or {})})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode(errors="replace")


def post_with_webhook(webhook, payload):
    try:
        http_post_json(webhook, payload)
    except urllib.error.HTTPError as e:
        sys.exit(f"Slack error {e.code}: {e.read().decode(errors='replace')} (check the SLACK_WEBHOOK_URL secret)")


def post_with_bot(token, channel, payload, thread_ts=None):
    """Post via the Slack API (needed for thread replies). Returns the message ts."""
    body = {"channel": channel, "unfurl_links": False, "unfurl_media": False, **payload}
    if thread_ts:
        body["thread_ts"] = thread_ts
    try:
        data = json.loads(http_post_json(
            "https://slack.com/api/chat.postMessage", body, {"Authorization": f"Bearer {token}"}))
    except urllib.error.HTTPError as e:
        sys.exit(f"Slack error {e.code}: {e.read().decode(errors='replace')}")
    if not data.get("ok"):
        hints = {
            "not_in_channel": "invite the app to the channel: type /invite @Overdue Report in it",
            "channel_not_found": "check the SLACK_CHANNEL_ID secret, and invite the app to the channel",
            "invalid_auth": "check the SLACK_BOT_TOKEN secret",
            "missing_scope": "add the chat:write permission to the Slack app and reinstall it",
        }
        err = data.get("error")
        sys.exit(f"Slack error: {err} ({hints.get(err, 'see https://api.slack.com/methods/chat.postMessage')})")
    return data["ts"]


def to_plain_text(payload):
    """Rough plain-text rendering of the Slack blocks for --dry-run."""
    out = []
    for b in payload["blocks"]:
        if b["type"] == "header":
            out.append("== " + b["text"]["text"] + " ==")
        elif b["type"] == "divider":
            out.append("-" * 60)
        elif b["type"] == "section":
            out.append(b["text"]["text"].rstrip())
        elif b["type"] == "context":
            out.append("  " + " ".join(e["text"] for e in b["elements"]))
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--from-file")
    ap.add_argument("--today", help="override today's date (YYYY-MM-DD), for testing")
    args = ap.parse_args()

    today = datetime.strptime(args.today, "%Y-%m-%d").date() if args.today else today_local()

    if args.from_file:
        with open(args.from_file) as f:
            tasks = json.load(f)
    else:
        token = os.environ.get("CLICKUP_API_TOKEN", "").strip()
        if not token:
            sys.exit("Missing CLICKUP_API_TOKEN secret.")
        tasks = fetch_overdue_tasks(token, start_of_day_ms(today))

    bot_token = os.environ.get("SLACK_BOT_TOKEN", "").strip()
    channel = os.environ.get("SLACK_CHANNEL_ID", "").strip()
    use_bot = bool(bot_token and channel)

    payload, replies = build_message(build_items(tasks, today), today, threads=use_bot or args.dry_run)

    if args.dry_run:
        print(to_plain_text(payload))
        for r in replies:
            print("\n   ↳ THREAD REPLY")
            print("\n".join("   " + line for line in to_plain_text(r).splitlines()))
        return

    if use_bot:
        ts = post_with_bot(bot_token, channel, payload)
        for r in replies:
            post_with_bot(bot_token, channel, r, thread_ts=ts)
        print(f"Posted report for {today} with {len(replies)} thread replies.")
        return

    webhook = os.environ.get("SLACK_WEBHOOK_URL", "").strip()
    if not webhook:
        sys.exit("Missing Slack secrets: set SLACK_BOT_TOKEN + SLACK_CHANNEL_ID (or SLACK_WEBHOOK_URL).")
    post_with_webhook(webhook, payload)
    print(f"Posted report for {today}.")


if __name__ == "__main__":
    main()
