#!/usr/bin/env python3
"""
Generate a PDF from a cv-variant.md (or cv.md) file using the approved HTML template.

Usage:
    python3 scripts/generate-cv-pdf.py opportunities/safetica-senior-pm/cv-variant.md

Output is saved alongside the source file as cv-<firstname>-<company>.pdf
If the source is context/cv.md, output goes to context/cv-<firstname>.pdf
"""

import sys
import os
import re
import html

# ---------------------------------------------------------------------------
# Markdown CV parser
# ---------------------------------------------------------------------------

def parse_cv_markdown(text):
    """Parse a cv-variant.md (or cv.md) into structured data."""
    data = {
        "name": "",
        "contact": {},  # location, email, phone, linkedin, website
        "summary": "",
        "experience": [],  # list of roles
        "skills": [],  # list of {category, items}
        "education": [],  # list of {degree, school, dates}
    }

    # Strip YAML-ish front matter / metadata block (lines starting with >)
    lines = text.split("\n")

    # Remove HTML comments (tailoring notes etc.)
    text_clean = re.sub(r"<!--[\s\S]*?-->", "", text)
    lines = text_clean.split("\n")

    # Find sections by ## headings
    sections = {}
    current_section = None
    current_lines = []

    for line in lines:
        m = re.match(r"^##\s+(.+)", line)
        if m:
            if current_section:
                sections[current_section] = "\n".join(current_lines)
            current_section = m.group(1).strip()
            current_lines = []
        elif current_section:
            current_lines.append(line)

    if current_section:
        sections[current_section] = "\n".join(current_lines)

    # --- Contact ---
    if "Contact Information" in sections:
        ci = sections["Contact Information"]
        for line in ci.split("\n"):
            line = line.strip()
            m = re.match(r"\*\*Name:\*\*\s*(.+)", line)
            if m:
                data["name"] = m.group(1).strip()
            m = re.match(r"\*\*Location:\*\*\s*(.+)", line)
            if m:
                data["contact"]["location"] = m.group(1).strip()
            m = re.match(r"\*\*Email:\*\*\s*(.+)", line)
            if m:
                data["contact"]["email"] = m.group(1).strip()
            m = re.match(r"\*\*Phone:\*\*\s*(.+)", line)
            if m:
                data["contact"]["phone"] = m.group(1).strip()
            m = re.match(r"\*\*LinkedIn:\*\*\s*(.+)", line)
            if m:
                data["contact"]["linkedin"] = m.group(1).strip()
            m = re.match(r"\*\*Website:\*\*\s*(.+)", line)
            if m:
                data["contact"]["website"] = m.group(1).strip()

    # --- Summary ---
    if "Professional Summary" in sections:
        data["summary"] = sections["Professional Summary"].strip().strip("-").strip()

    # --- Experience ---
    if "Experience" in sections:
        exp_text = sections["Experience"]
        # Split by ### headings (company names)
        role_blocks = re.split(r"(?=^### )", exp_text, flags=re.MULTILINE)
        for block in role_blocks:
            block = block.strip()
            if not block.startswith("###"):
                continue
            block_lines = block.split("\n")
            company = re.sub(r"^###\s+", "", block_lines[0]).strip()

            # There may be multiple roles within one company block
            # Each role starts with **Title** | dates
            roles_in_block = []
            i = 1
            while i < len(block_lines):
                line = block_lines[i].strip()
                role_match = re.match(r"\*\*(.+?)\*\*\s*\|?\s*(.*)", line)
                if role_match:
                    title = role_match.group(1).strip()
                    rest = role_match.group(2).strip()
                    # Extract parenthetical note (e.g., "progressed from Technical PM")
                    note = ""
                    paren_match = re.search(r"\((.+?)\)", rest)
                    if paren_match:
                        note = paren_match.group(1)
                        rest = rest[:paren_match.start()] + rest[paren_match.end():]
                    # After removing the paren, extract dates from what remains
                    # Strip leading pipes, whitespace, and stray markdown markers
                    dates_clean = rest.strip().lstrip("|").strip().strip("*").strip()

                    # Next line might be location
                    location = ""
                    i += 1
                    if i < len(block_lines):
                        loc_line = block_lines[i].strip()
                        if loc_line and not loc_line.startswith("-") and not loc_line.startswith("*"):
                            location = loc_line
                            i += 1

                    # Collect bullet points
                    achievements = []
                    while i < len(block_lines):
                        bline = block_lines[i].strip()
                        if bline.startswith("- "):
                            # Strip markdown bold markers for cleaner PDF output
                            bullet = bline[2:].strip()
                            bullet = re.sub(r"\*\*(.+?)\*\*", r"\1", bullet)
                            achievements.append(bullet)
                            i += 1
                        elif bline.startswith("---"):
                            i += 1
                            break
                        elif bline == "":
                            i += 1
                        else:
                            break

                    roles_in_block.append({
                        "title": title,
                        "dates": dates_clean,
                        "company": company,
                        "location": location,
                        "note": note,
                        "achievements": achievements,
                    })
                else:
                    i += 1

            data["experience"].extend(roles_in_block)

    # --- Skills ---
    if "Skills" in sections:
        sk_text = sections["Skills"]
        for line in sk_text.split("\n"):
            line = line.strip()
            m = re.match(r"\*\*(.+?):\*\*\s*(.+)", line)
            if m:
                data["skills"].append({
                    "category": m.group(1).strip(),
                    "items": m.group(2).strip(),
                })

    # --- Education ---
    if "Education" in sections:
        edu_text = sections["Education"]
        edu_blocks = re.split(r"(?=^### )", edu_text, flags=re.MULTILINE)
        for block in edu_blocks:
            block = block.strip()
            if not block.startswith("###"):
                continue
            block_lines = block.split("\n")
            school = re.sub(r"^###\s+", "", block_lines[0]).strip()
            degree = ""
            dates = ""
            for eline in block_lines[1:]:
                eline = eline.strip()
                m = re.match(r"\*\*(.+?)\*\*\s*\|?\s*(.*)", eline)
                if m:
                    degree = m.group(1).strip()
                    dates = m.group(2).strip()
            data["education"].append({
                "degree": degree,
                "school": school,
                "dates": dates,
            })

    return data


# ---------------------------------------------------------------------------
# HTML builder
# ---------------------------------------------------------------------------

def escape(text):
    return html.escape(text)


def build_contact_items(contact):
    items = []
    if contact.get("location"):
        items.append(f'<span>{escape(contact["location"])}</span>')
    if contact.get("email"):
        items.append(f'<span>{escape(contact["email"])}</span>')
    if contact.get("phone"):
        items.append(f'<span>{escape(contact["phone"])}</span>')
    if contact.get("linkedin"):
        url = contact["linkedin"]
        if not url.startswith("http"):
            url = "https://" + url
        items.append(f'<span><a href="{escape(url)}">{escape(contact["linkedin"])}</a></span>')
    if contact.get("website"):
        url = contact["website"]
        if not url.startswith("http"):
            url = "https://" + url
        items.append(f'<span><a href="{escape(url)}">{escape(contact["website"])}</a></span>')
    return "\n    ".join(items)


def build_experience_blocks(experience):
    blocks = []
    for role in experience:
        company_parts = [escape(role["company"])]
        if role.get("location"):
            company_parts.append(escape(role["location"]))
        if role.get("note"):
            company_parts.append(escape(role["note"]))
        company_line = " · ".join(company_parts)

        bullets = "\n".join(
            f"      <li>{escape(a)}</li>" for a in role["achievements"]
        )

        block = f"""  <div class="job">
    <div class="job-title-line">
      <span class="job-title">{escape(role['title'])}</span>
      <span class="job-dates">{escape(role['dates'])}</span>
    </div>
    <div class="job-company">{company_line}</div>
    <ul>
{bullets}
    </ul>
  </div>"""
        blocks.append(block)
    return "\n\n".join(blocks)


def build_skills_blocks(skills):
    blocks = []
    for s in skills:
        blocks.append(
            f'  <div class="skills-row">\n'
            f'    <span class="skills-label">{escape(s["category"])}: </span>\n'
            f'    <span class="skills-value">{escape(s["items"])}</span>\n'
            f'  </div>'
        )
    return "\n".join(blocks)


def build_education_blocks(education):
    blocks = []
    for e in education:
        blocks.append(
            f'  <div class="edu-item">\n'
            f'    <div class="edu-left"><span class="edu-name">{escape(e["degree"])}</span>'
            f' <span class="edu-school">— {escape(e["school"])}</span></div>\n'
            f'    <span class="edu-dates">{escape(e["dates"])}</span>\n'
            f'  </div>'
        )
    return "\n".join(blocks)


def populate_template(template_html, data):
    out = template_html
    out = out.replace("{{name}}", escape(data["name"]))
    out = out.replace("{{contact_items}}", build_contact_items(data["contact"]))
    out = out.replace("{{summary}}", escape(data["summary"]))
    out = out.replace("{{experience_blocks}}", build_experience_blocks(data["experience"]))
    out = out.replace("{{skills_blocks}}", build_skills_blocks(data["skills"]))
    out = out.replace("{{education_blocks}}", build_education_blocks(data["education"]))
    return out


# ---------------------------------------------------------------------------
# PDF generation
# ---------------------------------------------------------------------------

def find_chromium_binary():
    """Find a Chromium-based browser for headless PDF generation."""
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    # Try PATH
    import shutil
    for name in ["google-chrome", "chromium", "brave-browser"]:
        found = shutil.which(name)
        if found:
            return found
    return None


def generate_pdf(html_string, output_path):
    """Generate PDF using headless Chromium with no browser artifacts."""
    import subprocess
    import tempfile

    browser = find_chromium_binary()
    if not browser:
        print("ERROR: No Chromium-based browser found. Install Chrome, Chromium, or Brave.")
        sys.exit(1)

    # Write HTML to a temp file so the browser can load it
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8") as tmp:
        tmp.write(html_string)
        tmp_path = tmp.name

    try:
        result = subprocess.run(
            [
                browser,
                "--headless",
                "--disable-gpu",
                "--no-pdf-header-footer",
                "--print-to-pdf-no-header",
                f"--print-to-pdf={output_path}",
                tmp_path,
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            print(f"Browser stderr: {result.stderr}")
        if not os.path.isfile(output_path):
            print("ERROR: PDF was not created. Browser output:")
            print(result.stderr)
            sys.exit(1)
    finally:
        os.unlink(tmp_path)


# ---------------------------------------------------------------------------
# Output path logic
# ---------------------------------------------------------------------------

def determine_output_path(source_path, name):
    first_name = name.split()[0].lower() if name else "cv"
    source_dir = os.path.dirname(source_path)
    source_base = os.path.basename(source_dir)

    if "opportunities" in source_path:
        # opportunities/safetica-senior-pm/cv-variant.md -> cv-martin-safetica-senior-pm.pdf
        company = source_base
        filename = f"cv-{first_name}-{company}.pdf"
        return os.path.join(source_dir, filename)
    else:
        # context/cv.md -> context/cv-martin.pdf
        filename = f"cv-{first_name}.pdf"
        return os.path.join(source_dir, filename)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/generate-cv-pdf.py <path-to-cv-variant.md>")
        sys.exit(1)

    source_path = sys.argv[1]
    if not os.path.isfile(source_path):
        print(f"ERROR: File not found: {source_path}")
        sys.exit(1)

    # Resolve paths relative to project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_path = os.path.join(project_root, "templates", "cv-pdf-template.html")

    if not os.path.isfile(template_path):
        print(f"ERROR: Template not found: {template_path}")
        sys.exit(1)

    with open(source_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template_html = f.read()

    data = parse_cv_markdown(md_content)
    populated_html = populate_template(template_html, data)
    output_path = determine_output_path(source_path, data["name"])

    generate_pdf(populated_html, output_path)
    print(f"PDF saved to: {output_path}")

    # Also save the populated HTML for debugging
    html_debug_path = output_path.replace(".pdf", ".html")
    with open(html_debug_path, "w", encoding="utf-8") as f:
        f.write(populated_html)
    print(f"Debug HTML saved to: {html_debug_path}")


if __name__ == "__main__":
    main()
