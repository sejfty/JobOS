# n8n Setup Guide for JobOS Job Scout

> This guide walks you through setting up the n8n workflow that powers Module 0 (Job Scout).
> Estimated setup time: 15-20 minutes.

---

## Prerequisites

- Docker Desktop installed ([download](https://www.docker.com/products/docker-desktop/))
- An Anthropic API key ([get one](https://console.anthropic.com/))
- A job board API key — the workflow ships with an Adzuna source as a sample ([get a free key](https://developer.adzuna.com/))
- JobOS repo cloned locally
- `context/target-roles.md` and `context/profile.md` populated (Module 1 should be complete)

---

## Step 1: Start n8n with Docker

Create `docker-compose.yml` in the `n8n/` folder of your JobOS repo:

```yaml
services:
  n8n:
    image: docker.n8n.io/n8nio/n8n
    ports:
      - "5678:5678"
    volumes:
      - n8n_data:/home/node/.n8n
      - /ABSOLUTE/PATH/TO/jobos/scouting:/data/scouting
      - /ABSOLUTE/PATH/TO/jobos/context:/data/context:ro
    environment:
      - N8N_SECURE_COOKIE=false
      - N8N_RESTRICT_FILE_ACCESS_TO=/data/
volumes:
  n8n_data:
```

**Important:** Replace `/ABSOLUTE/PATH/TO/jobos/` with the actual path to your JobOS repo (e.g., `/Users/yourname/Projects/jobos/`).

**Volume mounts explained:**
- `scouting/` is mounted read-write — n8n writes the scout report here
- `context/` is mounted read-only (`:ro`) — n8n reads your target criteria and profile but cannot modify them
- n8n has no access to any other folders on your machine

Start n8n:

```bash
cd n8n/
docker compose up -d
```

Open http://localhost:5678 in your browser. Create an owner account on first launch.

---

## Step 2: Import the Workflow

1. In n8n, click the three dots (⋯) in the top-right → **Import from File**
2. Select `n8n/jobos-scout-workflow.json`
3. The workflow will appear in your workflow list

---

## Step 3: Configure API Keys

The workflow requires two API keys, both entered directly in workflow nodes:

**Anthropic API key (for scoring):**
1. Open the workflow and find the **"Call Claude API"** Code node
2. Find the line containing `'x-api-key': 'YOUR_ANTHROPIC_API_KEY_HERE'`
3. Replace the placeholder with your actual Anthropic API key

**Adzuna API key (for job fetching):**
1. Find the **"Fetch Adzuna"** HTTP Request node
2. In the Query Parameters, replace the `app_id` and `app_key` values with your Adzuna credentials

---

## Step 4: Test

1. Open the workflow in the editor
2. Click **"Execute Workflow"** to run it manually
3. Check that `scouting/scout-report.md` was created in your JobOS repo
4. Review the output — the first run is a good opportunity to calibrate scoring quality

---

## Step 5: Publish and Activate

For the workflow to run automatically, it must be **published**:

1. Click the **"Publish"** button in the top-right corner of the workflow editor
2. Once published, the workflow's **n8n Trigger** node fires every time the n8n container starts

The workflow includes a built-in once-per-day guard: it checks the last run timestamp in the scout report and exits silently if less than 20 hours have passed. Even if n8n starts multiple times per day, the scouting workflow only runs once.

---

## Step 6: Automatic Startup (Optional)

To have n8n start automatically when your machine starts:
- Open Docker Desktop → Settings → General → enable **"Start Docker Desktop when you sign in to your computer"**

When Docker starts, it starts the n8n container. When n8n starts, the published workflow triggers. The guard ensures it runs once per day.

---

## Adding More Job Sources

The workflow ships with a single sample source — **Adzuna (GB)** — to demonstrate the pipeline. You can add more sources by duplicating the fetch branch pattern:

1. From the IF node's "true" output, add a new **HTTP Request** node for your source
2. Add a **Code** node after it that normalizes results into the standard format (same fields as the existing Normalize Listings node: id, source, title, company, location, url, date_posted, description, salary_min, salary_max, salary_currency)
3. Connect the normalize node to the **Merge All** node as an additional input

**Adding more Adzuna countries:** Duplicate the "Fetch Adzuna" node and change the country code in the URL — `gb`, `de`, `at`, `nl`, `fr`, `us`, etc. Each country needs its own fetch node. Update the salary_currency in the normalize step accordingly.

**Adding other job boards:** Any API or RSS feed that returns job listings can be added as a new branch. The only requirement is that the normalize step outputs the same standard format. The scoring and reporting pipeline downstream works regardless of where listings came from.

---

## Troubleshooting

**n8n can't read files:** Check that docker-compose volume paths are correct and use absolute paths. Verify with: `docker exec -it n8n-n8n-1 ls /data/context/`

**"Access to the file is not allowed" error:** Make sure `N8N_RESTRICT_FILE_ACCESS_TO=/data/` is set in docker-compose.yml. Restart the container after adding it: `docker compose down && docker compose up -d`

**Workflow doesn't run on startup:** Make sure the workflow is **published** (not just saved). Check Executions tab in n8n to see if it ran.

**Scoring quality is poor:** Review the scoring prompt in the "Build Scoring Prompt" Code node. Common issues: truncated job descriptions (Adzuna limitation — adding sources with full JDs improves results), overly conservative scoring (adjust tier definitions in the prompt), missing transferable skill recognition (add domain-specific guidance).

**Safari shows errors:** The `N8N_SECURE_COOKIE=false` environment variable (already in the docker-compose template) fixes this.

**n8n won't start:** Make sure Docker Desktop is running first. Check logs: `docker compose logs`
