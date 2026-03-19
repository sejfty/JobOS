"""
Shared markdown CV parser and output path logic.
Used by generate-cv-pdf.py and generate-cv-docx.py.
"""

import os
import re


def parse_cv_markdown(text):
    """Parse a cv-variant.md (or cv.md) into structured data."""
    data = {
        "name": "",
        "contact": {},  # location, email, phone, linkedin, website
        "summary": "",
        "personal_project": [],  # list of projects with title, subtitle, achievements
        "experience": [],  # list of roles
        "skills": [],  # list of {category, items}
        "education": [],  # list of {degree, school, dates}
    }

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
        data["experience"] = _parse_role_blocks(exp_text)

    # --- Personal Project ---
    for section_name in sections:
        if section_name.lower().startswith("personal project"):
            pp_text = sections[section_name]
            pp_blocks = re.split(r"(?=^### )", pp_text, flags=re.MULTILINE)
            for block in pp_blocks:
                block = block.strip()
                if not block.startswith("###"):
                    continue
                block_lines = block.split("\n")
                title = re.sub(r"^###\s+", "", block_lines[0]).strip()

                # Next line might be subtitle (bold + link + date)
                subtitle = ""
                i = 1
                if i < len(block_lines):
                    sub_line = block_lines[i].strip()
                    if sub_line.startswith("**") or sub_line.startswith("["):
                        subtitle = re.sub(r"\*\*(.+?)\*\*", r"\1", sub_line)
                        i += 1

                # Collect bullets
                achievements = []
                while i < len(block_lines):
                    bline = block_lines[i].strip()
                    if bline.startswith("- "):
                        bullet = bline[2:].strip()
                        bullet = re.sub(r"\*\*(.+?)\*\*", r"\1", bullet)
                        achievements.append(bullet)
                        i += 1
                    elif bline.startswith("---"):
                        break
                    elif bline == "":
                        i += 1
                    else:
                        break

                data["personal_project"].append({
                    "title": title,
                    "subtitle": subtitle,
                    "achievements": achievements,
                })
            break

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


def _parse_role_blocks(exp_text):
    """Parse experience section into list of role dicts."""
    roles = []
    role_blocks = re.split(r"(?=^### )", exp_text, flags=re.MULTILINE)
    for block in role_blocks:
        block = block.strip()
        if not block.startswith("###"):
            continue
        block_lines = block.split("\n")
        company = re.sub(r"^###\s+", "", block_lines[0]).strip()

        i = 1
        while i < len(block_lines):
            line = block_lines[i].strip()
            role_match = re.match(r"\*\*(.+?)\*\*\s*\|?\s*(.*)", line)
            if role_match:
                title = role_match.group(1).strip()
                rest = role_match.group(2).strip()
                # Extract parenthetical note
                note = ""
                paren_match = re.search(r"\((.+?)\)", rest)
                if paren_match:
                    note = paren_match.group(1)
                    rest = rest[:paren_match.start()] + rest[paren_match.end():]
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

                roles.append({
                    "title": title,
                    "dates": dates_clean,
                    "company": company,
                    "location": location,
                    "note": note,
                    "achievements": achievements,
                })
            else:
                i += 1

    return roles


def determine_output_path(source_path, name):
    first_name = name.split()[0].lower() if name else "cv"
    source_dir = os.path.dirname(source_path)
    source_base = os.path.basename(source_dir)

    if "opportunities" in source_path:
        company = source_base
        filename = f"cv-{first_name}-{company}.pdf"
        return os.path.join(source_dir, filename)
    else:
        filename = f"cv-{first_name}.pdf"
        return os.path.join(source_dir, filename)
