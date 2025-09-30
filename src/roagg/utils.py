import importlib.metadata
import re

def match_patterns(string, patterns):
    if string is None:
        return False

    for pattern in patterns:
        # if pattern does not contain * or ? check if string contains pattern
        if '*' not in pattern and '?' not in pattern:
            if pattern.lower() is string.lower() or pattern.lower() in string.lower():
                return True
    
        
        if re.match(pattern_to_regexp(pattern), string, re.IGNORECASE):
            return True
    return False

def pattern_to_regexp(pattern: str) -> str:
    regex = ""
    for char in pattern:
        if char == '*':
            regex += '.*'
        elif char == '?':
            regex += '.'
        else:
            regex += re.escape(char)
    return '^' + regex + '$'

def get_roagg_version() -> str:
    """Get package version from metadata."""
    try:
        return importlib.metadata.version("roagg")
    except importlib.metadata.PackageNotFoundError:
        return "unknown"