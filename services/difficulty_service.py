def calculate_difficulty(code):
    score = 0
    lines = code.split("\n")

    patterns = [
        "for ", "while ", "if ", "else", "elif",
        "def ", "function ", "class ",
        "try", "except", "catch",
        "async", "await"
    ]

    # Pattern complexity
    for p in patterns:
        if p in code:
            score += 1

    # Large code boost
    if len(lines) > 50:
        score += 2

    # Decision
    if score <= 4:
        return "Beginner"
    elif score <= 8:
        return "Intermediate"
    return "Advanced"
