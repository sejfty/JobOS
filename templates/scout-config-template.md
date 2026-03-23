# Job Scout Configuration

> Copy this file to `scouting/scout-config.md` and fill in your job search sources.
> The n8n workflow reads this file at the start of each scouting run.
> Add or remove sources at any time — changes take effect on the next run.

---

## Job Boards

<!-- Add one section per job board. Each board needs its own keywords and filters. -->
<!-- Supported source types: API (requires API key in n8n), RSS feed, or career page URL. -->

### [Board Name]
- Keywords: [comma-separated search terms, e.g., product manager, product lead, head of product]
- Location: [geographic filter, e.g., Europe, Remote, US]
- Seniority: [level filter if supported, e.g., senior, lead, director]

<!-- Example:
### Adzuna
- Keywords: product manager, product lead, head of product
- Location: Europe, Remote
- Seniority: senior, lead, director

### Remotive
- Keywords: product manager, product lead
- Category: product
-->

---

## Company Watch List

<!-- Add companies whose career pages you want monitored for new PM roles. -->
<!-- The scout report will always surface new PM postings from these companies, -->
<!-- regardless of how they score against your criteria. -->

### [Company Name]
- Careers URL: [full URL to the company's careers/jobs page]

<!-- Example:
### Miro
- Careers URL: https://miro.com/careers/

### Productboard
- Careers URL: https://www.productboard.com/careers/
-->
