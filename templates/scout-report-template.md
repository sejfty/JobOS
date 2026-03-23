# Scout Report Format Reference

> This file documents the expected format of `scouting/scout-report.md`.
> The n8n workflow generates this format automatically. Do not edit scout-report.md manually.
> This template exists as documentation of the interface contract between n8n and JobOS.

---

## Expected Structure

The scout report is a rolling file. Each daily run prepends a new section at the top. Sections are separated by `---`. The scout agent reads the most recent unreviewed section.

```
# Job Scout Report

## YYYY-MM-DD

> Sources: [list of sources queried] | Company Watch: [list of watched companies checked]
> Found: [total raw] | Deduped: [after dedup] | Watch: [count] | Strong: [count] | Aspirational: [count] | Experience Fit: [count] | Skipped: [count]

### Company Watch

**[Company] — [Job Title]**
Careers page: [URL]
Posted: [date]
Score: [tier assignment]
Match: [2-3 sentences on match rationale]
Flags: [concerns or notes, omit if none]

### Strong Match

**[Company] — [Job Title]**
Source: [source] | [Location] | Posted: [date]
URL: [url]
Match: [2-3 sentences]
Flags: [if any]

### Worth a Look — Aspirational

**[Company] — [Job Title]**
Source: [source] | [Location] | Posted: [date]
URL: [url]
Match: [what aligns with target + what's a stretch on profile]
Flags: [what's missing]

### Worth a Look — Experience Fit

**[Company] — [Job Title]**
Source: [source] | [Location] | Posted: [date]
URL: [url]
Match: [why profile is strong + why outside target but interesting]
Flags: [if any]

### Skipped

[count] listings filtered: [reason] ([count]), [reason] ([count]), ...
```

## Review Markers

When the user reviews a section via the scout agent, the agent appends:

```
✓ Reviewed YYYY-MM-DD
```

The planning advisor checks for sections without this marker to create todo items.

## Archival

Sections older than 30 days are moved to `scouting/scout-archive.md` by the n8n workflow during each run.
