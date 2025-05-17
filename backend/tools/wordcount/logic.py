def get_word_count(text: str) -> str:
    import re
    words = re.findall(r'\b\w+\b', text)
    count = len(words)
    return f"Word count: {count}"