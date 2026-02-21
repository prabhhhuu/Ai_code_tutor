import re

def format_ai_output(text):
    if not text:
        return ""

    # Remove unwanted markdown symbols
    text = re.sub(r"[#*`]", "", text)

    lines = [l.strip() for l in text.split("\n") if l.strip()]

    html = ""
    in_list = False
    in_code = False

    for line in lines:
        lower = line.lower()

        # Section headings
        if lower.startswith((
            "step", "bugs", "improvements",
            "time", "security", "explanation"
        )):
            if in_list:
                html += "</ul>"
                in_list = False
            if in_code:
                html += "</pre>"
                in_code = False

            html += f"<h3>{line}</h3>"
            continue

        # Code sections
        if lower.startswith((
            "improved code", "optimized code", "secure version"
        )):
            if in_list:
                html += "</ul>"
                in_list = False

            html += f"<h3>{line}</h3><pre class='code-block'>"
            in_code = True
            continue

        # Inside code block
        if in_code:
            html += line + "\n"
            continue

        # Bullet list
        if line.startswith("-"):
            if not in_list:
                html += "<ul>"
                in_list = True

            html += f"<li>{line[1:].strip()}</li>"
            continue

        # Numbered heading
        if line[0].isdigit() and "." in line:
            if in_list:
                html += "</ul>"
                in_list = False

            html += f"<p><strong>{line}</strong></p>"
            continue

        # Close list if needed
        if in_list:
            html += "</ul>"
            in_list = False

        html += f"<p>{line}</p>"

    if in_list:
        html += "</ul>"
    if in_code:
        html += "</pre>"

    return html
