# Daily Overdue-Task Report (ClickUp → Slack)

Every weekday at 8:00 AM Eastern, GitHub reads ClickUp and posts a summary of overdue work to a Slack channel. It runs on GitHub's servers, so your computer can be off.

**What it covers:** the Agency Clients, Operations and Growth spaces. It leaves out Templates Hub, closed or completed tasks, and archived tasks.
**"Overdue" means** the due date was before today (Eastern time). A task due today does not count yet.

The message shows:

1. A one-line summary: overdue team tasks (and how many have no assignee) and overdue client deadlines.
2. **Team tasks**, grouped by person and then by client, most overdue first. Each person shows up to 12 tasks, then "+N more".
3. **Unassigned** overdue tasks in their own section.
4. **Client deadlines** (tasks named `CLIENT DEADLINE | ...`): the client, what's owed, days overdue, and who follows up (the task's assignee).
5. If nothing is overdue, a one-line all-clear.

---

## One-time setup (about 15 minutes)

You'll create two "keys" and store them in GitHub as **secrets**. Secrets are encrypted. Nobody can see them after you save them, including you, and they never appear in the code.

### Step 1: Get your ClickUp API token

1. Log in to ClickUp as **Kyra**. The report sees only what this account can see, and the owner account can see everything.
2. Click your **profile picture** (bottom-left corner).
3. Click **Settings**.
4. In the left menu, click **Apps**.
5. Under **API Token**, click **Generate** (or **Copy** if one already exists).
6. Copy the token. It starts with `pk_`. Keep it in a safe place for Step 3, and don't paste it into Slack, email or chat.

### Step 2: Get a Slack webhook URL

A webhook is a private web address that lets the report post into one Slack channel.

1. Pick or create the channel the report should post to (for example `#daily-overdue`).
2. Go to **https://api.slack.com/apps** and sign in to your Slack workspace.
3. Click **Create New App** → **From scratch**.
4. App name: `Overdue Report`. Workspace: your agency's workspace. Click **Create App**.
5. In the left menu, click **Incoming Webhooks** and turn the switch **On**.
6. Scroll down and click **Add New Webhook to Workspace** (on some screens it's "Add New Webhook").
7. Choose the channel from item 1 and click **Allow**.
8. Back on the Incoming Webhooks page, copy the new **Webhook URL**. It starts with `https://hooks.slack.com/services/`.

*If Slack says you need approval, a Slack workspace admin has to approve the app first.*

### Step 3: Save both as GitHub secrets

1. Open this repository on GitHub.
2. Click **Settings** (top menu of the repo, far right).
3. In the left menu, click **Secrets and variables** → **Actions**.
4. Click **New repository secret**.
   - Name: `CLICKUP_API_TOKEN`
   - Secret: paste the `pk_...` token
   - Click **Add secret**
5. Click **New repository secret** again.
   - Name: `SLACK_WEBHOOK_URL`
   - Secret: paste the `https://hooks.slack.com/...` URL
   - Click **Add secret**

The names have to match exactly: all capitals, with underscores.

### Step 4: Test it

1. In the repo, click the **Actions** tab. If GitHub asks, click to enable workflows.
2. In the left list, click **Daily overdue report**.
3. Click **Run workflow** (right side). Leave **"Preview only"** ticked and click the green **Run workflow** button.
4. After about 30 seconds, click the run, then **report**, then open the **Build and send the report** step. The full report prints there. Nothing goes to Slack yet.
5. If the preview looks right, run it again with **"Preview only" unticked**. This time the report posts to your Slack channel.

### Step 5: Turn on the daily schedule

The schedule is **on**. To pause it, open `.github/workflows/overdue-report.yml`, put a `#` at the start of these three lines and commit:

```yaml
  schedule:
    - cron: "0 12 * * 1-5"   # 8 AM EDT (summer)
    - cron: "0 13 * * 1-5"   # 8 AM EST (winter)
```

(Or just ask Claude to do it.)

The two lines handle daylight saving time, and the workflow runs only the one that matches 8 AM Eastern. GitHub sometimes starts scheduled jobs **5–20 minutes late** when its servers are busy, so the post may land a little after 8:00.

---

## Changing things later

All settings are at the top of `overdue_report.py`:

| To change… | Edit |
|---|---|
| Team members | `TEAM` (ClickUp user ID → name) |
| Which spaces are included | `INCLUDED_SPACES` / `EXCLUDED_SPACES` |
| Tasks shown per person before "+N more" | `MAX_LINES_PER_SECTION` |

A task assigned to someone who isn't on the roster (for example Barbara Bedford) still appears under that person's name, marked "not on roster", so it doesn't get lost.

## Troubleshooting

- **The run fails with "ClickUp API error 401"**: the ClickUp token is wrong or was regenerated. Repeat Step 1 and update the secret (Settings → Secrets → `CLICKUP_API_TOKEN` → Update).
- **The run fails with "Slack error 404/403"**: the webhook was removed or the app was uninstalled. Repeat Step 2 and update `SLACK_WEBHOOK_URL`.
- **GitHub emails you that a run failed**: open the run in the Actions tab. The last lines of the log say what went wrong.
