import re
import unicodedata

def slugify_basic(text):
    # Normalize Unicode to closest ASCII representation
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    # Remove any character that is not a letter, number, dash, underscore, or space
    text = re.sub(r"[^\w\s-]", "", text)
    # Replace spaces and underscores/dashes with single dashes
    text = re.sub(r"[\s_-]+", "-", text)
    # Strip leading/trailing dashes and convert to lowercase
    return text.strip("-").lower()