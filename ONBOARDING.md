# Onboarding

This guide walks you through setting up JobOS and running your first workflow. It assumes you've read the [README](README.md) and have the prerequisites installed.

> **Your data stays on your machine.** All personal files — your profile, CV, target roles, opportunity data, and pipeline — are gitignored and never committed to the repository. The repo contains only the system itself (agent instructions, templates, scripts). When you clone JobOS, you bring the engine. Your data lives locally.

## Step 1 — Clone and open

```bash
git clone https://github.com/sejfty/JobOS.git
cd JobOS
```

Open the project in Claude Code — either directly in your terminal or through an IDE like Cursor. Claude Code automatically loads `CLAUDE.md` at the start of every session, which gives it full context about the project, the folder structure, and how every module works.

That's it for setup. There's nothing to install, no dependencies to configure, no config files to edit. The system runs entirely from markdown files and Claude Code.

## Step 2 — Set up your profile

Start by saying something like:

> "Help me set up my profile."

The system will create `context/profile.md` from the template automatically and walk you through it conversationally — your experience summary, strengths, work style, what energizes you, what drains you, and your career narrative. This file gives every downstream module a sense of who you are beyond your CV.

You can also fill it in manually by editing `context/profile.md` directly. The template has inline guidance explaining what each section expects.

## Step 3 — Define what you're looking for

Next:

> "Help me define what I'm looking for."

This triggers the Goal Setting workflow, which creates `context/target-roles.md` and guides you through target role types, industries, company size, geographic preferences, compensation expectations, must-haves, and deal-breakers. It will challenge vague answers — "product roles" isn't specific enough; "Senior Growth PM at a B2B SaaS scale-up" is.

This file shapes how every module evaluates fit and prioritizes advice. The more specific you are here, the better everything downstream gets.

## Step 4 — Import your CV

> "Parse my LinkedIn PDF."

Export your LinkedIn profile as a PDF (LinkedIn → Me → View Profile → More → Save to PDF), then provide the file to Claude Code. The system parses it into `context/cv.md` — your canonical CV in structured markdown.

After import, review the result carefully. LinkedIn profiles are often outdated or incomplete. Fix anything that's wrong, add missing detail, and let the system know when you're ready.

Alternatively, you can paste your existing CV content directly or fill in `context/cv.md` manually.

## Step 5 — Review and strengthen your CV

Once `cv.md` is populated, run the review process:

> "Review my CV."

The CV reviewer analyzes your base CV for weak spots — vague bullets, missing outcomes, gaps in how you present your experience. It will tell you specifically what needs fixing and why. This is where the Tough Love principle kicks in: expect direct, constructive criticism, not generic praise.

After making your updates, you can run the CV against two feedback personas for additional perspective:

> "Run the recruiter and CPO feedback on my CV."

The recruiter persona checks whether your CV is scannable, keyword-rich, and passes ATS filters. The CPO persona evaluates whether it demonstrates real product craft and impact. Together they cover both audiences your CV needs to work for.

This step matters. Everything downstream — tailored CVs, cover letters, interview prep — builds on `cv.md`. The stronger your base CV, the better every output gets.

## Step 6 — Start using the system

With your profile, targets, and a reviewed CV in place, you're ready to use any module. Here are some things you can say:

**Add an opportunity:**
> "I found a role I'm interested in — here's the JD: [paste URL or text]"
> "I want to track Acme Corp — I reached out to their recruiter but they don't have a PM role listed yet."

**Tailor your CV for a specific role:**
> "Tailor my CV for this role." (from within an opportunity context)

**Get planning advice:**
> "What should I focus on today?"
> "Had a screening call with Acme, went well, they want a case study next week."

**Research a company:**
> "Research this company for me."

**Optimize your LinkedIn profile:**
> "Optimize my LinkedIn profile."

You don't need to memorize commands. Just describe what you want in natural language and the system routes to the right workflow.

## What happens behind the scenes

When you interact with the system, it reads the relevant agent file from `agents/`, loads your context files, and produces outputs into the right locations. Everything about a single opportunity lives in one folder under `opportunities/`.

The system will tell you when something is missing. If you skip ahead and jump straight to CV tailoring without setting up your profile or target roles, it won't block you — but it will flag what's missing and explain what you're losing. You can always go back and fill in context files later.

## Optional — Daily digest notification

If you're on macOS, you can set up a daily notification that summarizes your pending tasks and nudges you to run a planning session:

```bash
cd notifications
chmod +x setup.sh jobos-notify.sh
./setup.sh
```

It asks for your repo path and preferred notification time. Uses only built-in macOS tools. The system works fine without it. See [`notifications/README.md`](notifications/README.md) for details.

## Optional: LinkedIn MCP for Enhanced Company Research

JobOS can connect to your LinkedIn to pull richer data during company research — leadership profiles, PM team composition, and hiring patterns. This is optional. Without it, company research still works using web search, with reduced depth for LinkedIn-dependent sections.

**MCP Server:** `stickerdaniel/linkedin-mcp-server` (https://github.com/stickerdaniel/linkedin-mcp-server)

**Prerequisites:** `uv` must be installed. Then install the browser dependency:
```bash
uvx patchright install chromium
```

**Step 1 — Authenticate with LinkedIn:**
```bash
uvx linkedin-scraper-mcp --login
```
This opens a browser window. Log into LinkedIn manually — handle 2FA and captcha if prompted. This creates a persistent browser profile at `~/.linkedin-mcp/`.

**Step 2 — Register with Claude Code:**
```bash
claude mcp add linkedin -- uvx linkedin-scraper-mcp
```

**Step 3 — Verify:**
Start a Claude Code session and type `/mcp`. Confirm `linkedin` shows as connected.

**Troubleshooting:**
- Sessions expire periodically. Re-run `uvx linkedin-scraper-mcp --login` to re-authenticate.
- LinkedIn may present captcha challenges. Solve manually in the browser window.
- This uses browser-based scraping, not LinkedIn's official API. Works for personal low-volume use.

## Optional: Job Scout (Module 0) — Automated Job Discovery

Every module in JobOS assumes you already have a job posting to work with. Module 0 solves the step before that: finding relevant opportunities automatically so you don't have to manually scan job boards, career pages, and LinkedIn every day.

An n8n workflow runs daily in the background on your machine. It fetches listings from job board APIs and RSS feeds you configure, scores each one against your target roles and professional profile using the Claude API, and writes a curated scout report to `scouting/scout-report.md`. You review the matches in Claude Code and promote interesting ones into your pipeline with a single command — the same Entry Gate flow used for any manually found opportunity.

This is the only module that requires tooling beyond Claude Code:

- **Docker Desktop** — runs n8n locally
- **n8n** — the workflow automation platform (free, self-hosted)
- **Anthropic API key** — for AI-powered scoring of listings against your profile (~$5/month at daily runs)
- **Job board API key(s)** — the workflow ships with one sample source (Adzuna, UK listings) to demonstrate the full pipeline. You should add sources relevant to your search — more Adzuna countries, other job board APIs, RSS feeds, or company career pages

Once Module 0 is running, the planning advisor (Module 2) automatically detects new scout reports and creates todo items to review them. Automated discovery stays connected to your daily workflow without extra effort.

**Setup:** Follow the step-by-step guide in [`n8n/N8N-SETUP.md`](n8n/N8N-SETUP.md) for installation and configuration.

---

## Recommended order vs. reality

The steps above are the recommended order: profile → target roles → CV → CV review → opportunities → modules. This gives the system maximum context to work with from the start.

But JobOS is designed to be flexible. If you want to jump straight to adding an opportunity and tailoring your CV, go ahead. The system will work with whatever context it has and flag what's missing. You can always circle back.
