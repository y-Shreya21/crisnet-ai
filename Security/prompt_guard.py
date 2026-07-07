import re

def sanitize_input(text: str) -> str:
    """
    Analyzes input text for security threats, including prompt injection,
    malicious OS commands, path traversals, and potential tool abuse attempts.
    Raises ValueError if a security threat is identified.
    Returns the cleaned location string on success.
    """
    if not isinstance(text, str):
        raise TypeError("Input text must be a string.")

    cleaned = text.strip()

    # 1. Size Constraints (Avoid buffer attacks or LLM context spamming)
    if len(cleaned) > 100:
        raise ValueError(f"Input exceeds maximum safe size (100 characters). Length: {len(cleaned)}")

    # 2. Path Traversal & OS Command Injections Detection
    dangerous_os_patterns = [
        r"\.\./",                      # Path traversal
        r"/etc/passwd",                # Unix system file access
        r"cmd\.exe",                   # Windows command prompt
        r"\b(rm|mv|cp|chmod|chown)\b", # Basic destructive linux shell tools
        r"\b(bash|sh|zsh|powershell|cmd|sudo)\b", # Shell environments
        r"\|\s*\w+",                   # Pipe executions
        r"&\s*\w+",                    # Background run or chains
        r"\$\(.*\)",                   # Command expansion
        r"`.*`",                       # Backtick execution
        r"<script.*?>",                # HTML tag script
        r"</script>",
        r"javascript:",                # JS scheme
        r"SELECT\s+.*?\s+FROM",        # SQL SELECT
        r"UNION\s+SELECT",             # SQL UNION
        r"DROP\s+TABLE",               # SQL DROP
        r"exec\s*\(",                  # Code exec
        r"system\s*\(",
    ]
    for pattern in dangerous_os_patterns:
        if re.search(pattern, cleaned, re.IGNORECASE):
            raise ValueError("Potential command injection, SQL/Script exploit, or unauthorized traversal pattern detected.")

    # 3. Prompt Injection Detection (System Instruction Overrides)
    prompt_injection_patterns = [
        r"ignore\s+(all\s+)?(previous\s+)?instructions",
        r"bypass\s+rules",
        r"you\s+are\s+now\s+a",
        r"act\s+as\s+a",
        r"new\s+system\s+directive",
        r"forget\s+what\s+I\s+said",
        r"system\s+override",
        r"jailbreak",
        r"developer\s+mode",
    ]
    for pattern in prompt_injection_patterns:
        if re.search(pattern, cleaned, re.IGNORECASE):
            raise ValueError("Prompt injection or system directive override attempt detected.")

    # 4. Tool Abuse & URI Scheme Abuse Prevention
    tool_abuse_patterns = [
        r"\b(http|https|ftp|file|gopher)://", # Block direct URIs in inputs
        r"\bapi_key\b",
        r"\btoken\b",
        r"\{\s*\{.*?\}\s*\}",                 # Template injections
    ]
    for pattern in tool_abuse_patterns:
        if re.search(pattern, cleaned, re.IGNORECASE):
            raise ValueError("Potential tool parameter manipulation or URI scheme injection detected.")

    # 5. Characters Whitelisting
    # Standard names for places can include letters, numbers, spaces, periods, commas, apostrophes, hyphens, and parentheses.
    if not re.match(r"^[a-zA-Z0-9\s\.,\-'\(\)]+$", cleaned):
        raise ValueError("Input contains characters violating safety white-list criteria.")

    return cleaned
