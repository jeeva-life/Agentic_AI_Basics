import re
from typing import Dict, Any
from datetime import datetime

def create_metadata(
    video_id: str,
    transcript_length: int,
    raw_transcript_length: int,
    video_metadata: str
) -> Dict[str, Any]:
    """Create metadata dictionary for workflow state"""
    return {
        'video_id': video_id,
        'transcript_length': transcript_length,
        'raw_transcript_length': raw_transcript_length,
        'video_metadata': video_metadata,
        'processed_at': datetime.now().isoformat(),
        'workflow_version': '2.0.0'
    }

def calculate_readability_score(text: str) -> float:
    """Calculate Flesch Reading Ease score for text"""
    try:
        sentences = [s for s in text.split('.') if s.strip()]
        words = text.split()
        syllables = count_syllables(text)
        
        if len(sentences) == 0 or len(words) == 0:
            return 0.0
        
        # Flesch Reading Ease formula
        score = 206.835 - (1.015 * (len(words) / len(sentences))) - (84.6 * (syllables / len(words)))
        
        return max(0.0, min(100.0, score))
        
    except Exception:
        return 50.0  # Default score if calculation fails

def count_syllables(text: str) -> int:
    """Count syllables in text (simplified approach)"""
    text = text.lower()
    count = 0
    vowels = "aeiouy"
    on_vowel = False
    
    for char in text:
        is_vowel = char in vowels
        if is_vowel and not on_vowel:
            count += 1
        on_vowel = is_vowel
    
    # Add one for words ending in 'e' (common in English)
    if text.endswith('e'):
        count -= 1
    
    return max(1, count)  # At least one syllable per word

def extract_hashtags(text: str) -> list:
    """Extract hashtags from text"""
    return re.findall(r'#\w+', text)

def extract_mentions(text: str) -> list:
    """Extract mentions from text"""
    return re.findall(r'@\w+', text)

def count_emojis(text: str) -> int:
    """Count emoji characters in text"""
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE
    )
    return len(emoji_pattern.findall(text))

def format_for_platform(content: str, platform: str) -> str:
    """Format content for specific platform"""
    if platform == "linkedin":
        return format_for_linkedin(content)
    elif platform == "twitter":
        return format_for_twitter(content)
    elif platform == "blog":
        return format_for_blog(content)
    else:
        return content

def format_for_linkedin(content: str) -> str:
    """Format content specifically for LinkedIn"""
    # Add LinkedIn-specific formatting
    lines = content.split('\n')
    formatted_lines = []
    
    for line in lines:
        if line.strip():
            # Add bullet points for lists
            if line.strip().startswith('-') or line.strip().startswith('•'):
                formatted_lines.append(line)
            elif line.strip().startswith(('1.', '2.', '3.', '4.', '5.')):
                formatted_lines.append(line)
            else:
                formatted_lines.append(line)
    
    return '\n'.join(formatted_lines)

def format_for_twitter(content: str) -> str:
    """Format content specifically for Twitter"""
    # Ensure content fits Twitter limits
    if len(content) > 280:
        # Truncate and add continuation indicator
        return content[:277] + "..."
    return content

def format_for_blog(content: str) -> str:
    """Format content specifically for blog"""
    # Add blog-specific formatting
    lines = content.split('\n')
    formatted_lines = []
    
    for line in lines:
        if line.strip():
            # Add markdown formatting for headings
            if line.strip().isupper() and len(line.strip()) < 50:
                formatted_lines.append(f"## {line.strip()}")
            else:
                formatted_lines.append(line)
    
    return '\n'.join(formatted_lines) 