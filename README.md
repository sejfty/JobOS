# JobOS

A Claude Code project that helps product managers navigate a job search systematically. Think of it as a PM operating system — but for finding your next role instead of building product.

---

## What It Is

JobOS is a collection of markdown context files, agent instructions, and workflow templates stored in a GitHub repository and run inside Claude Code. You bring your CV, your goals, and your job opportunities. The system helps you tailor your application, prepare for interviews, track your pipeline, and research companies — all grounded in your actual experience, with direct and honest feedback.

### Who It's For

Product managers who are actively job searching and want a structured, AI-assisted system to work smarter — not a chatbot that tells them their CV is great.

---

## Core Principles

These two principles are the project's DNA. They run through every module and every output.

### Honesty

The system works exclusively with verified, real information provided by the user. It never fabricates, exaggerates, or implies experience, skills, or achievements that don't exist.

When a gap is identified between what a role requires and what the user has, the system flags it transparently rather than papering over it. A tailored CV only reorders and rewords what's true — it never invents. A cover letter doesn't oversell. Interview prep doesn't coach bluffing.

### Tough Love

All system outputs are constructively critical and direct. Better to struggle in preparation than fail in the real thing.

Weak CV points are called out. If an interview answer would fall flat with a real VP Product, the system says so. If a target role is unrealistic given the user's experience, it flags it. No generic praise, no sugarcoating.

---

## How the System Works

JobOS is structured in three layers:

```
┌─────────────────────────────────────────────────────┐
│                   MODULE LAYER                      │
│  M1  M2  M3  M4  M5  M6  M7  M8                     │
├─────────────────────────────────────────────────────┤
│                   ENTRY GATE                        │
│           opportunity.md (per job)                  │
├─────────────────────────────────────────────────────┤
│                FOUNDATION LAYER                     │
│  profile.md | cv.md | target-roles.md | CLAUDE.md   │
└─────────────────────────────────────────────────────┘
```

**Foundation Layer** — Context files that represent the user's identity: their CV, professional profile, and target role criteria. `CLAUDE.md` is loaded automatically by Claude Code every session, so every module starts with full project context.

**Entry Gate** — Every opportunity enters through one mechanism with two paths. **JD-first:** the user provides a URL (or pastes JD text as fallback), and the system normalizes it into a full `opportunity.md` file (stage: Saved). **Company-first:** the user wants to track a company before a specific role exists — recruiter outreach, networking, speculative interest — and the system creates a minimal `opportunity.md` with just the company name and a context note (stage: Exploring). When a JD appears later, it flows into the existing folder. All downstream modules read from `opportunity.md` — modules that require a JD gracefully stop for Exploring-stage opportunities.

**Module Layer** — Eight capability modules built incrementally. Each has its own agent instruction file in `agents/`. Modules are triggered by natural language — "tailor my CV for this role" or "I need a cover letter" — and Claude Code routes to the right agent.

---

## Modules

| # | Module | Status | Description |
|---|--------|--------|-------------|
| 1 | Goal Setting | Designed | Define target roles, industries, must-haves, and deal-breakers before applying anywhere |
| 2 | Pipeline & Planning | Designed | Track application stages (Exploring → Saved → ... → Offer) and get proactive, opinionated recommendations on what to do next |
| 3 | CV Optimization | Designed | LinkedIn PDF → canonical CV → one-time review → per-opportunity tailoring → PDF + DOCX output. CVs are optimized to pass AI-powered ATS screening — structural formatting and keyword alignment are handled automatically during review and tailoring. Also generates LinkedIn-optimized profile content — different in tone, depth, and keyword strategy from the CV — for manual profile update. |
| 4 | Cover Letter Writing | Designed | Generate a specific, authentic cover letter from your CV + JD + company context |
| 5 | Homework Assignment Help | Designed | Support for take-home tasks and case studies, grounded in your actual knowledge |
| 6 | Interview Simulation | TBD | Agents role-play as VP Product, recruiter, and hiring manager for realistic practice |
| 7 | Interview Analysis & Feedback Loop | TBD | Analyze real interview transcripts → identify patterns → feed back into future prep |
| 8 | Company Intelligence | Designed | Comprehensive company research — business health, product analysis, and employee sentiment in one report. Single trigger, single output. |
| | *(Modules 9–10 merged into Module 8)* | | *Employee sentiment and product analysis are now sections within Module 8. Interview question generation will be part of Module 6.* |

**Designed** = detailed design complete, ready to build.
**TBD** = intent is clear, detailed design still needed. Flagged honestly rather than guessed at.

---

## Getting Started

See [SETUP.md](SETUP.md) for step-by-step setup instructions. *(Coming soon — will be written once the full workflow is validated.)*

The short version: clone the repo, open it in Claude Code, and start a workflow. Claude Code will automatically create the context files from the templates in `templates/` the first time they're needed — you just fill them in.

### Recommended Setup Order

1. **`context/profile.md`** — Start here. Your professional identity, strengths, work style, and career narrative. This gives every downstream module a sense of who you are beyond your CV.
2. **`context/target-roles.md`** — What you're looking for: role types, industries, company size, must-haves, deal-breakers. You can fill this in directly or use the Goal Setting workflow (Module 1) to work through it. This shapes how modules evaluate fit and prioritize advice.
3. **Any module workflow** — Once your profile and targets are set, every module has the context it needs to give you its best output.

You don't have to follow this order. If you jump straight to CV optimization or opportunity entry, the system will tell you which context files are missing and why they matter — then continue with whatever it has. Nothing blocks.

---

## Repository Structure

```
jobos/
├── CLAUDE.md                     ← AI instruction file (auto-loaded by Claude Code)
├── README.md                     ← this file
│
├── context/                      ← your personal data — gitignored, never committed
│   ├── profile.md                ← your professional identity (auto-created from template)
│   ├── cv.md                     ← your canonical CV (auto-created from template)
│   └── target-roles.md           ← what you're looking for (auto-created from template)
│
├── templates/                    ← blank starter templates (committed to repo)
│   ├── profile-template.md       ← starter for context/profile.md
│   ├── cv-template.md            ← starter for context/cv.md
│   ├── target-roles-template.md  ← starter for context/target-roles.md
│   ├── opportunity-template.md
│   ├── cv-variant-template.md
│   ├── cover-letter-template.md
│   └── company-research-template.md  ← template for Module 8 output
│
├── agents/                       ← agent instruction files (added as modules are built)
├── notifications/                ← optional: daily macOS notification for pending tasks
├── pipeline.md                   ← summary of all in-flight opportunities (gitignored)
└── opportunities/                ← one folder per job application (gitignored)
```

---

## Daily Digest Notification

An optional macOS notification that summarizes your pending tasks from `todo.md` and nudges you to run a planning session. Runs once daily at a time you choose — useful if you want a reminder to keep your search moving without opening the repo.

To set it up, run `./notifications/setup.sh` and enter your repo path and preferred time. It uses only built-in macOS tools (no dependencies). The system works fine without it.

See [`notifications/README.md`](notifications/README.md) for full details, including uninstall and troubleshooting.

---

## Using This as a Template

If you're cloning this for your own job search:

1. Clone the repo and open it in Claude Code. Your personal files (`context/profile.md`, `context/cv.md`, `context/target-roles.md`) are gitignored — they stay on your machine, never in the repo.
2. Claude Code will automatically create each context file from the corresponding template in `templates/` the first time a workflow needs it. Fill in your own information when prompted.
3. Nothing in the system assumes anything about who you are — all context flows from the files you populate.
4. The agent instructions in `agents/` will work for any PM, not just the original author.
