def build_prompt(code, language, mode):
    base = f"""
You are a professional coding tutor.

IMPORTANT RULES:
- No markdown
- Plain clean text

Code ({language}):
{code}
"""
    if mode == "explain":
        return base + "Step-by-Step Explanation:\nExplain clearly."
    if mode == "improve":
        return base + "Rewrite improved version."
    if mode == "optimize":
        return base + "Rewrite optimized version."
    if mode == "security":
        return base + "List security issues and fix."
    return base
