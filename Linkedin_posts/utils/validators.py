import re
from urllib.parse import urlparse, parse_qs
from typing import Optional

def extract_youtube_video_id(url: str) -> Optional[str]:
    """Extract YouTube video ID from various URL formats"""
    if not url:
        return None
    
    # Common YouTube URL patterns
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'youtube\.com\/watch\?.*v=([^&\n?#]+)',
        r'youtu\.be\/([^&\n?#]+)',
        r'youtube\.com\/embed\/([^&\n?#]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            video_id = match.group(1)
            # Validate video ID format (11 characters, alphanumeric, hyphens, underscores)
            if re.match(r'^[a-zA-Z0-9_-]{11}$', video_id):
                return video_id
    
    return None

def validate_youtube_url(url: str) -> bool:
    """Validate if URL is a valid YouTube URL"""
    video_id = extract_youtube_video_id(url)
    return video_id is not None

def validate_output_format(format_type: str) -> bool:
    """Validate output format type"""
    valid_formats = ["linkedin", "blog", "article", "twitter"]
    return format_type.lower() in valid_formats

def validate_language(language: str) -> bool:
    """Validate language code"""
    # Common language codes
    valid_languages = [
        "en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh",
        "ar", "hi", "bn", "ur", "tr", "nl", "sv", "da", "no", "fi"
    ]
    return language.lower() in valid_languages

def sanitize_text(text: str) -> str:
    """Sanitize text input"""
    if not text:
        return ""
    
    # Remove potentially harmful characters
    sanitized = re.sub(r'[<>"\']', '', text)
    
    # Remove excessive whitespace
    sanitized = re.sub(r'\s+', ' ', sanitized)
    
    return sanitized.strip()

def validate_content_length(content: str, platform: str) -> bool:
    """Validate content length for specific platform"""
    if not content:
        return False
    
    length = len(content)
    
    if platform == "linkedin":
        return length <= 3000
    elif platform == "twitter":
        return length <= 280
    elif platform == "blog":
        return length >= 100  # Minimum length for blog
    else:
        return True  # No specific limit for other platforms

def extract_domain_from_url(url: str) -> Optional[str]:
    """Extract domain from URL"""
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except Exception:
        return None

def is_valid_url(url: str) -> bool:
    """Check if URL is valid"""
    try:
        parsed = urlparse(url)
        return all([parsed.scheme, parsed.netloc])
    except Exception:
        return False 