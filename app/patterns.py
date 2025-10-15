# app/patterns.py
patterns = {
    "Email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}",
    "Credit Card": r"\b(?:\d[ -]*?){13,16}\b",
    "Phone Number": r"\b(\+98|0)?9\d{9}\b",
    "Password": r"(?i)password|passwd|pwd",
    "API Key": r"(?i)api[_-]?key|secret|token",
}
