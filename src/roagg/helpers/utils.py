import importlib.metadata
import re

doi_pattern = re.compile(r'^10\.\d{4,9}/[-._;()/:A-Z0-9]+$', re.IGNORECASE)

def is_valid_doi(s: str) -> bool:
    return bool(doi_pattern.match(s))

def find_doi_in_text(text: str) -> str | None:
    return re.findall(r'\b10\.\d{4,9}/[-.;()/:\w]+', text)

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

def string_word_count(string: str) -> int:
    """Count words in a string after trimming whitespace."""
    if not string:
        return 0
    return len(string.strip().split())