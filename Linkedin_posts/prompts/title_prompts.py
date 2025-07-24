from langchain_core.prompts import PromptTemplate

TITLE_GENERATION_PROMPT = PromptTemplate(
    input_variables=["transcript", "content_analysis", "trend_info", "output_format"],
    template="""
    Generate an engaging title for content based on the following information:
    
    Transcript: {transcript}
    Content Analysis: {content_analysis}
    Trend Information: {trend_info}
    Output Format: {output_format}
    
    Guidelines for {output_format} titles:
    - Make it engaging and clickable
    - Include relevant keywords
    - Keep it concise but descriptive
    - Use power words when appropriate
    - Consider current trends and interests
    - Match the professional tone for {output_format}
    
    Generate 3 title options, ranked by engagement potential:
    
    1. [Most Engaging]
    2. [Alternative Option]
    3. [Conservative Option]
    
    Best Title:
    """
)

TITLE_OPTIMIZATION_PROMPT = PromptTemplate(
    input_variables=["title", "platform"],
    template="""
    Optimize the following title for {platform}:
    
    Original Title: {title}
    
    Platform-specific optimization guidelines:
    
    For LinkedIn:
    - Professional and business-focused
    - Include industry-relevant keywords
    - Avoid clickbait but maintain engagement
    - Consider thought leadership angle
    
    For Twitter:
    - Concise and impactful
    - Include relevant hashtags
    - Create curiosity and urgency
    - Optimize for retweet potential
    
    For Blog:
    - SEO-optimized with keywords
    - Clear and descriptive
    - Include benefit or value proposition
    - Consider long-tail keywords
    
    For General Articles:
    - Balanced approach
    - Clear and informative
    - Engaging but not sensational
    - Accessible to broad audience
    
    Optimized Title:
    """
) 