# New-Client Onboarding (GHL → ClickUp + welcome email)

When a client pays a proposal in GoHighLevel, this runs on its own within about a minute:

1. **Chooses the account manager** by open clients against each pod's cap, and posts the counts it used.
2. **Builds the client's ClickUp folder** in **Agency Clients**. It copies every list and task in *Templates Hub → Sage Social Studio - Client Template*, adds a dated **Onboarding Timeline** (copied from *Client Onboarding Timeline*), and assigns all of it to the chosen AM.
3. **Sends the client a welcome email from GHL.** It assigns the contact to the AM and fills in the AM's name, email and booking link. Then it adds the tag `onboarding - am assigned`, which starts your welcome-email workflow in GHL.
4. **Posts to Slack:** the new client, who got them, and everyone's capacity at that moment.

If anything fails, Slack gets a 🚨 message with a link to the log, and GitHub emails you.

### How the account manager is chosen

It goes by **open clients only**. A client counts as open for someone while they have at least one open task in that client's folder in Agency Clients.

- Account managers are grouped into **pods**, and each pod has a cap on open clients. **Bella + Campbell share one pod, capped at 10.** A client both of them work on counts once.
- A new client goes to the pod with the **most open slots** (cap minus open clients).
- Inside a pod, it goes to the member with **fewer open clients**. That person gets the ClickUp tasks and the GHL contact.
- If every pod is at its cap, it still assigns the least-full pod and flags it in Slack, so a client is never left without an owner.

---

## One-time setup (about 30 minutes)

### Step 1: Check the pods

Open `onboarding.py` and look at `PODS` near the top:

- `max_clients`: the pod's cap on open clients (Bella/Campbell: 10; Hailey: 10 is a placeholder to confirm)
- `booking_link` (on each person above `PODS`): their GHL calendar link for the onboarding call
- `active`: `False` stops a pod getting new clients

### Step 2: GHL contact fields

In GHL go to **Settings → Custom Fields**, then add three **Contact** fields with these exact names (type: single line):

- `Account Manager Name`
- `Account Manager Email`
- `Account Manager Booking Link`

Make sure each AM is also a **user** in GHL with the same email as in `ACCOUNT_MANAGERS`, so the contact can be assigned to them.

### Step 3: GHL API key and location ID

1. GHL → **Settings → Private Integrations → Create new integration**. Name it `Onboarding automation`.
2. Choose these scopes: **View/Edit Contacts**, **View Users**, **View Custom Fields** (`contacts.readonly`, `contacts.write`, `users.readonly`, `locations/customFields.readonly`).
3. Copy the token. It starts with `pit-`.
4. Your **location ID** is in the browser address bar inside the sub-account: `app.gohighlevel.com/v2/location/`**`THIS_PART`**`/...`

### Step 4: A GitHub key for GHL

GHL needs this key to start the GitHub workflow.

1. On GitHub, go to your picture → **Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token**.
2. Name: `GHL onboarding`. Expiration: 1 year (set a reminder to renew it).
3. **Repository access → Only select repositories → TikTok.**
4. **Permissions → Repository permissions → Contents → Read and write.** Leave everything else alone.
5. Generate and copy the token. It starts with `github_pat_`. This key can only touch this one repository.

### Step 5: Save the secrets in GitHub

In this repo, go to **Settings → Secrets and variables → Actions → New repository secret**. Add:

| Name | Value |
|---|---|
| `GHL_API_TOKEN` | the `pit-...` token from Step 3 |
| `GHL_LOCATION_ID` | the location ID from Step 3 |
| `ONBOARDING_SLACK_CHANNEL_ID` | *(optional)* channel for new-client posts. If you leave it out, posts go to the overdue-report channel. Invite the Slack app to the channel with `/invite @Overdue Report`. |

`CLICKUP_API_TOKEN` and `SLACK_BOT_TOKEN` are already there from the overdue report.

### Step 6: GHL workflow 1, "Proposal paid → start onboarding"

In GHL go to **Automation → Workflows → Create workflow → Start from scratch**.

1. **Trigger:** **Payment Received**. Add a filter so it only fires for proposals: **Payment source** is **Documents & Contracts** (or **Invoice**, if your proposals create an invoice). *If your GHL shows these slightly differently, pick the option that matches a proposal payment.*
2. **If/Else:** contact **Tags** → **does not include** `client - active`. This stops monthly or repeat payments from re-onboarding an existing client. Put the next step on the "yes" branch.
3. **Action: Custom Webhook**
   - **Method:** POST
   - **URL:** `https://api.github.com/repos/sageinteriordesignmarketing/TikTok/dispatches`
   - **Headers:**
     - `Authorization`: `Bearer github_pat_...` (the token from Step 4)
     - `Accept`: `application/vnd.github+json`
   - **Body** (raw JSON):

```json
{
  "event_type": "ghl-proposal-paid",
  "client_payload": {
    "contact_id": "{{contact.id}}",
    "first_name": "{{contact.first_name}}",
    "last_name": "{{contact.last_name}}",
    "email": "{{contact.email}}",
    "phone": "{{contact.phone}}",
    "company": "{{contact.company_name}}",
    "package": "",
    "amount": "",
    "account_manager": ""
  }
}
```

   For `package` and `amount`, pick the payment's product name and amount from the merge-field picker (**{} → Payment**). They're optional and only show in Slack.

4. Save and **Publish**.

### Step 7: GHL workflow 2, "Welcome email"

1. **Trigger:** **Contact Tag** → tag added → `onboarding - am assigned`.
2. **Action: Send Email.** Draft below; adjust it to your voice. Add your onboarding form link.

> **Subject:** Welcome to Sage, {{contact.first_name}}! Here's what happens next
>
> Hi {{contact.first_name}},
>
> We're so excited to start working with you! Your payment came through, and your account is all set up on our end.
>
> **Meet your account manager:** {{contact.account_manager_name}} will be your main point of contact, and you can reach them anytime at {{contact.account_manager_email}}.
>
> **Your next two steps:**
> 1. **Fill out your onboarding form** (about 15 minutes): [ONBOARDING FORM LINK]. It covers your brand, goals and account access, so we can get started on your strategy right away.
> 2. **Book your onboarding/strategy call** with {{contact.account_manager_name}}: {{contact.account_manager_booking_link}}
>
> Here's how your first month looks:
> - **Week 1:** strategy, research and your onboarding call
> - **Week 2:** we build your first 2–4 weeks of content for your approval
> - **Week 3:** posting begins
> - **Day 30:** your first analytics report
>
> Talk soon,
> The Sage team

   *GHL may name these merge fields slightly differently (for example `{{contact.account_manager_booking_link}}`). Insert them with the **{}** picker to be sure.*

3. *(Optional)* add **Internal Notification → email the assigned user** so the AM gets a heads-up too.
4. Save and **Publish**.

### Step 8: Test it

1. In GitHub, go to **Actions → New client onboarding → Run workflow**.
2. Enter a test contact's GHL **contact ID** and a company name like `TEST Client`. Leave **Preview only** ticked.
3. Open the run and read the log. It shows who would be chosen, what would be built, and the Slack message. **Nothing is changed.**
4. Untick **Preview only** to do it for real, then check ClickUp, the GHL contact and Slack. Delete the `TEST Client` folder afterwards.
5. Last, make a small real payment on a test proposal in GHL to check the full chain.

---

## Changing things later

Everything is at the top of `onboarding.py`:

| To change… | Edit |
|---|---|
| Who's in which pod, and each pod's client cap | `PODS` |
| Which template gets copied | `CLIENT_TEMPLATE_FOLDER`, `ONBOARDING_TIMELINE_LIST` |
| The GHL tag that sends the welcome email | `GHL_TRIGGER_TAG` |

To change the folder structure, edit the template in **Templates Hub**. New clients get whatever is there. In the timeline, a task whose name (or parent's name) contains **"Day N"** or **"Day N–M"** gets a due date N (or M) days after payment.

**Picking the AM yourself:** put their name in `account_manager` in the webhook body, or in the box when running it by hand.

## Troubleshooting

- **Slack says "every pod is at its client cap":** the client still got an owner, but it's time to rebalance or hire.
- **Open-client counts look too high:** a finished client still has open tasks in its folder. Close or archive those tasks (or the folder) and they stop counting.
- **The client got no welcome email:** check the GHL contact has the `onboarding - am assigned` tag and that workflow 2 is published. If the Slack post shows a ⚠️ about GHL, it says what failed.
- **The run never started:** in GHL, open workflow 1's execution log. A 401 or 404 on the webhook usually means the GitHub token expired or is missing **Contents: Read and write**.
- **A client paid but already had a folder:** nothing is copied twice. The folder is matched by name.
