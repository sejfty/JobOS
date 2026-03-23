# n8n Setup Guide for JobOS Job Scout

> This guide walks you through setting up the n8n workflow that powers Module 0 (Job Scout).
> Estimated setup time: 15-20 minutes.

---

## Prerequisites

- Docker Desktop installed ([download](https://www.docker.com/products/docker-desktop/))
- An Anthropic API key ([get one](https://console.anthropic.com/))
- JobOS repo cloned locally
- `context/target-roles.md` and `context/profile.md` populated (Module 1 should be complete)
- `scouting/scout-config.md` filled in with at least one job board source

---

## Step 1: Start n8n with Docker

Create or edit `docker-compose.yml` in the `n8n/` folder:

```yaml
version: "3"
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
volumes:
  n8n_data:
```

**Important:** Replace `/ABSOLUTE/PATH/TO/jobos/` with the actual path to your JobOS repo (e.g., `/Users/yourname/Projects/jobos/`).

Start n8n:

```bash
cd n8n/
docker compose up -d
```

Open http://localhost:5678 in your browser. Create an owner account on first launch.

---

## Step 2: Import the Workflow

1. In n8n, click the three dots (...) in the top-right → Import from File
2. Select `n8n/jobos-scout-workflow.json`
3. The workflow will appear in your workflow list

---

## Step 3: Configure Credentials

1. Go to Credentials in the n8n sidebar
2. Add a new Anthropic credential with your API key
3. Open the imported workflow and connect the Anthropic credential to the Claude API scoring node
4. If you're using job board APIs that require keys (e.g., Adzuna), add those credentials too

---

## Step 4: Configure File Paths

The workflow reads and writes files using paths inside the Docker container:
- `/data/context/target-roles.md` — your target criteria (read-only)
- `/data/context/profile.md` — your professional profile (read-only)
- `/data/scouting/scout-config.md` — your job board configuration
- `/data/scouting/scout-report.md` — the scout report output

These paths are pre-configured in the workflow. If your docker-compose volume mounts are correct, no changes are needed.

---

## Step 5: Test

1. Open the workflow in the editor
2. Click "Execute Workflow" to run it manually
3. Check that `scouting/scout-report.md` was created/updated in your JobOS repo
4. Review the output — the first run is a good opportunity to calibrate scoring quality

---

## Step 6: Automatic Startup (Optional)

To have n8n start automatically when your machine wakes up, create a macOS launchd plist or simply start Docker Desktop at login (Docker Desktop has this option in Settings → General → "Start Docker Desktop when you sign in").

The workflow includes a built-in guard: it checks the last run timestamp and exits if less than 20 hours have passed. Even if n8n starts multiple times per day, the scouting workflow only runs once.

---

## Troubleshooting

**n8n can't read files:** Check that docker-compose volume paths are correct and use absolute paths. Run `docker exec -it n8n-n8n-1 ls /data/context/` to verify files are visible inside the container.

**Scoring quality is poor:** Review the scoring prompt in the Claude API node. The prompt is designed to be edited — adjust tier thresholds or transferable skills emphasis based on your experience.

**Safari shows errors:** The `N8N_SECURE_COOKIE=false` environment variable (already in the docker-compose template) fixes this.

**n8n won't start:** Make sure Docker Desktop is running first. Check `docker compose logs` for error details.
