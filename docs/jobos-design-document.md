# JobOS — Design Document

> **Purpose:** High-level project overview — what it is, why it exists, core principles, and key decisions.
> **Companion files:** `jobos-architecture.md` (detailed architecture), `jobos-visualization-guide.md` (instructions for generating HTML visualization)

---

## What Is JobOS?

JobOS is a Claude Code project — a collection of markdown context files, agent instructions, and workflow templates stored in a GitHub repository — that helps product managers navigate a job search systematically. Think of it as a PMOS (Product Manager Operating System) but for finding your next role instead of building product.

### Triple Purpose

1. **Personal use** — the creator (Martin) will use it for his own PM job search
2. **Portfolio piece** — a tangible, working project to showcase during interviews, demonstrating product thinking, AI fluency, and hands-on execution
3. **Open source** — shared on GitHub for other PMs in the same situation

Because of purpose #3, the system must be **generalizable**. Context files are templates any PM can fill in. Agent instructions work regardless of who's using the system. Nothing is hardcoded to one person.

---

## Core Principles

These two principles are the project's DNA. They are embedded in every module, every agent instruction, every output. Non-negotiable.

### Principle 1: Honesty

The system works exclusively with verified, real information provided by the user. It never fabricates, exaggerates, or implies experience, skills, or achievements that don't exist.

When a gap is identified between what a role requires and what the user has, the system flags it transparently rather than papering over it.

**In practice across modules:**
- CV tailoring only reorders, emphasizes, and rewords what's true — never invents
- If a JD requires experience the user doesn't have, the system says so
- Cover letters don't oversell
- Homework help produces work based on the user's actual knowledge — not polished fiction that can't survive a follow-up conversation
- Interview simulation doesn't coach bluffing

### Principle 2: Tough Love

All system outputs are constructively critical and direct. Better to struggle in preparation than fail in the real thing.

**In practice across modules:**
- Weak CV points are called out clearly
- If an interview answer would fall flat with a real VP Product, the system says so
- If a target role is unrealistic given the user's experience, the system flags it
- Interview simulations challenge rather than coddle
- Post-interview analysis is honest about what went poorly

---

## Capability Modules

Modules are built incrementally, one at a time, as needed. The architecture supports all modules from the start so adding new ones doesn't break existing ones. Originally ten modules — Modules 9 and 10 were merged into Module 8.

| # | Module | Status | Notes |
|---|--------|--------|-------|
| 1 | Goal Setting | Designed | Define target roles, industries, must-haves, deal-breakers |
| 2 | Pipeline & Planning | Designed | Active planning advisor — captures activity, recommends next actions, tracks commitments |
| 3 | CV Optimization | Designed | LinkedIn PDF → cv.md → one-time review → per-opportunity tailoring → PDF |
| 4 | Cover Letter Writing | Designed | Uses base CV + JD + company context |
| 5 | Homework Assignment Help | Designed | Support for take-home tasks and case studies |
| 6 | Interview Simulation | TBD | Agents role-play as VP Product, recruiter, hiring manager |
| 7 | Interview Analysis & Feedback Loop | TBD | User provides real interview transcripts → system analyzes → feeds into future prep |
| 8 | Company Intelligence | Designed | Comprehensive company research — business health, product analysis, employee sentiment in one report. Modules 9 and 10 merged here. Interview question generation moved to Module 6. |

**"Designed"** = we have enough understanding to build it.
**"TBD"** = we know what it should do, but the detailed design still needs work. Flagged honestly rather than guessed at.

### Build Order

**First batch — build in this order:**
1. **Foundation** — CLAUDE.md, folder structure, README.md, context file templates (profile.md, cv.md, target-roles.md), opportunity template. Everything else depends on this.
2. **CV Optimization** (Module 3) — immediate need
3. **Goal Setting** (Module 1) — populates target-roles.md
4. **Pipeline & Planning** (Module 2) — becomes useful as opportunities accumulate

**Later — add as needed:**
- Modules 4 and 5 can be added quickly (relatively simple).
- Module 8 (Company Intelligence) — needed when evaluating opportunities.
- Modules 6 and 7 are complex but high-value — build when approaching interview stage.
- Module 8 (Company Intelligence) now includes what was previously Modules 9 and 10.

---

## Opportunity Input Flow

Every opportunity enters the system through one gate, with two entry paths:

**Path A — JD-first:**
1. User provides a URL to the job posting → system fetches and parses the JD
2. Fallback: if the URL can't be read (dynamic loading, paywall), user pastes the JD text directly
3. Output: full `opportunity.md` with JD, requirements, and metadata. Stage: Saved.

**Path B — Company-first (Exploring):**
1. User wants to track a company before a specific role exists — recruiter outreach, networking, speculative interest
2. Output: minimal `opportunity.md` with company name and a context note. JD fields left empty. Stage: Exploring.
3. When a JD appears later, the existing folder is updated (JD fields populated, folder renamed to include role, stage moved to Saved)

Folder naming: `company-name/` at Exploring stage, `company-name-role/` once a role is identified. This single entry point ensures every module works from the same source data. Modules that require a JD gracefully stop for Exploring-stage opportunities.

---

## CV Module — Detailed Design

This is the first module to build, so it has the most detail.

### Input Flow
1. User exports LinkedIn profile as PDF (standard LinkedIn feature)
2. System parses the PDF → extracts content → structures it into clean `cv.md`
3. User reviews and corrects (LinkedIn profiles are often outdated/incomplete)
4. One-time CV review suggests improvements to the base
5. User updates `cv.md` and mirrors changes to LinkedIn manually

### Per-Opportunity Tailoring
Given a specific JD, the system creates a CV variant. Tailoring rules (enforcing Principle 1):
- Can reorder sections to put relevant experience first
- Can emphasize existing skills that match the JD
- Can align terminology (if user did "intake-to-procure" work but JD uses different wording)
- CANNOT add skills the user doesn't have
- CANNOT inflate metrics, fabricate experience, or rewrite history
- If a gap exists → flag it: "This JD requires X. If you have this experience, add it to your base CV. If not, here's how to position what you do have."

### Dual Audience Awareness
CV must work for two distinct audiences:
- **Recruiters / headhunters** — keyword-scannable, matching standard PM terminology
- **VP Product / CPOs** — demonstrating product craft, thinking quality, and real impact

### PDF Output
One clean, professionally designed template. Single design — not multiple style options. Focus on getting typography and spacing right. Pipeline: markdown → HTML → PDF via Claude Code.

---

## Key Architecture Decisions

| Decision | Rationale |
|----------|-----------|
| Claude Code project (markdown + agents in GitHub repo) | Follows proven PMOS pattern; generalizable; version-controlled |
| Module-by-module build | Avoids scope paralysis; delivers value immediately |
| Architecture designed upfront for all modules | Adding modules later doesn't require restructuring |
| Per-opportunity folder structure | Everything about one application in one place |
| Single entry gate for opportunities | Consistent data format for all downstream modules |
| PDF generation included in project | User shouldn't need external tools to produce a sendable CV |
| Two core principles embedded in CLAUDE.md | Auto-loaded every session; also described in README.md for human readers |
| Separate agent files per module, shared defaults in CLAUDE.md | Focused prompts, better output quality, easier debugging; CLAUDE.md auto-loads shared behavior, no extra dependency hops |
| CLAUDE.md as project entry point + shared agent defaults | Auto-loaded by Claude Code; combines project orientation and behavioral defaults in one file — simpler than a separate shared-instructions.md |

---

## Required Deliverables

### Setup & Onboarding Guide
The project must ship with clear, step-by-step instructions for new users. A PM who clones the repo and opens it in Claude Code should know exactly what to do — which files to fill in first, in what order, what each template expects, and how to run their first workflow.

This guide will be built inside the project during the build phase, not during design. It should cover: prerequisites, which context files to populate first, how to add a new opportunity, how to trigger each module's workflow, and what to expect as output.

### Architecture Visualization
An HTML-based visual representation of the architecture (generated from `jobos-architecture.md`) for reviewing the system design. See `jobos-visualization-guide.md` for instructions.

---

## Open Design Questions

1. **Module 6 (Interview Simulation)** — TBD. How to prevent false confidence? Spoken vs typed responses? How many rounds per agent? Note: interview question generation (formerly Module 10) will be incorporated into Module 6.
2. **Module 7 (Feedback Loop)** — TBD. How does analysis from one interview feed into the next? Format for improvement tracking?
3. ~~**Module 8 (Company Intelligence)**~~ — **Resolved.** Narrative report with per-section confidence ratings (High/Medium/Low). Facts-first-opinion-second structure. See `agents/company-research-agent.md`.
4. ~~**Module 9 (Employee Sentiment)**~~ — **Resolved.** Merged into Module 8. Handled via Rule 8 (Honesty About Gaps): if no Glassdoor/Atmoskop data, say so directly and recommend interview questions to ask instead.
5. ~~**Module 10 (Product Deep Dive)**~~ — **Resolved.** Product analysis merged into Module 8. Interview question generation moved to Module 6.
6. **CV PDF template** — specific design decisions (fonts, layout, spacing) to be made during Module 3 build.

---

## Decision Log

| Date | Decision | Context |
|------|----------|---------|
| 2026-03-09 | Project concept defined | PMOS-like system for PM job search |
| 2026-03-09 | Ten modules identified | Full capability list established |
| 2026-03-09 | Principle 1: Honesty | Never fabricate, exaggerate, or imply false experience |
| 2026-03-09 | Principle 2: Tough Love | Constructively critical, no sugarcoating |
| 2026-03-09 | Opportunity input: URL primary, text fallback | Normalized into opportunity.md |
| 2026-03-09 | CV input: LinkedIn PDF export → cv.md | User reviews and corrects before use |
| 2026-03-09 | CV output: system-generated PDF, single template | Clean typography, one design |
| 2026-03-09 | CV tailoring: dual-audience aware | Recruiters vs VP Product/CPOs |
| 2026-03-09 | Build approach: module by module, architecture-first | Start with CV module |
| 2026-03-09 | Claude Project for design phase | Manage context across chat sessions |
| 2026-03-10 | Generalizable architecture | Templates, not hardcoded to one person |
| 2026-03-10 | Setup & onboarding guide required | Step-by-step instructions, built during build phase |
| 2026-03-10 | Architecture doc as separate file | Detailed component/module breakdown in jobos-architecture.md |
| 2026-03-10 | Architecture visualization as HTML | Generated from architecture doc, for visual review |
| 2026-03-10 | Modules 6-10 flagged as TBD | Honest about gaps — outline intent, don't fake detail |
| 2026-03-10 | Per-opportunity folder structure confirmed | Each opportunity gets its own folder with all related files |
| 2026-03-10 | Agent architecture: separate files per module, shared defaults in CLAUDE.md | Focused agent files; CLAUDE.md auto-loads project orientation + behavioral defaults; no separate shared-instructions.md needed |
| 2026-03-10 | CLAUDE.md as single entry point | Combines project orientation and shared agent behavior; auto-loaded by Claude Code, eliminates extra dependency hops |
| 2026-03-10 | PRINCIPLES.md removed — principles live in CLAUDE.md + README.md | CLAUDE.md for AI (auto-loaded), README.md for human readers; no separate file needed |
| 2026-03-10 | Build order confirmed | Foundation first, then Module 3 (CV), Module 1 (Goals), Module 2 (Pipeline) |
| 2026-03-17 | Module 2 redesigned: passive tracker → active planning advisor | Captures activity via natural language, recommends next actions across all opportunities, per-opportunity activity-log.md files |
| 2026-03-17 | Activity log simplified to 2 columns (Date, Activity) | Stage tracking lives in pipeline.md; activity descriptions capture all context naturally |
| 2026-03-17 | Cross-cutting rules: activity logging and pipeline.md updates | Any module logs opportunity-specific work to activity-log.md; any stage change triggers pipeline.md update |
| 2026-03-17 | todo.md added to Module 2 | Persistent action tracking — planning advisor writes committed items, reviews them each session, removes completed items |
| 2026-03-18 | Entry Gate supports pre-JD company tracking (Exploring stage) | Opportunity folders can be created with just a company name and context note. New Exploring stage precedes Saved. Folder renamed when JD arrives. All modules handle missing JD gracefully. |
| 2026-03-18 | Modules 8, 9, 10 merged into single Module 8: Company Intelligence | One trigger, one comprehensive output covering business health, product analysis, and employee sentiment. Simpler for the user — no need to run three separate modules. |
| 2026-03-18 | Interview question generation moved to Module 6 | Questions informed by company research belong in interview prep, not company research. Module 6 will read company-research.md when generating questions. |
| 2026-03-18 | Company research data sources: web search default, optional Tavily/Firecrawl upgrade | Agent checks for tool availability at start, falls back to web search. No hardcoded MCP integrations — designed for future extensibility. |
| 2026-03-18 | Company research: single agent file with internal separation | One agent covers all research areas. Refactor path to sub-modules if complexity grows, but single file is sufficient for now. |
| 2026-03-18 | Write-as-you-go workflow for company research | Research and write each section sequentially to manage context window and preserve partial output if interrupted. |
| 2026-03-18 | Per-section confidence levels (High/Medium/Low) | Every major section gets a confidence indicator with basis. Communicates data quality without hiding gaps. |
| 2026-03-18 | 3-week staleness threshold with lightweight refresh | Any module reading company-research.md older than 3 weeks flags it. Refresh updates changed sections without full re-run. |
| 2026-03-18 | Facts-first-opinion-second editorial approach | Each section: factual findings first, then editorial prefixed with "*Read:*". Keeps data and interpretation clearly separated. |
