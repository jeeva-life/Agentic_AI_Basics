from langchain_core.prompts import PromptTemplate

CONTENT_GENERATION_PROMPT = PromptTemplate(
    input_variables=["title", "transcript", "structure_analysis", "output_format"],
    template="""
    You are an expert AI researcher and technical analyst specializing in Artificial Intelligence, Machine Learning, Large Language Models, Multi-Agent Systems, and related technologies. Create a comprehensive technical summary of the AI/Agents video content. Focus ONLY on explaining the technical concepts, methods, and insights discussed in the video with the depth and accuracy expected from a domain expert.

    Title: {title}
    Transcript: {transcript}
    Structure Analysis: {structure_analysis}
    Output Format: {output_format}

    EXPERT REQUIREMENTS:
    1. **COMPREHENSIVE TECHNICAL ANALYSIS** - Analyze the entire transcript with expert-level understanding
    2. **AI/AGENTS DOMAIN EXPERTISE** - Apply deep knowledge of AI, ML, LLMs, Agents, and related technologies
    3. **TECHNICAL ACCURACY** - Ensure all technical concepts, methodologies, and terminology are precisely explained
    4. **NO PROMOTIONAL LANGUAGE** - Avoid phrases like "join us", "explore with us", "dive into", "let's discover"
    5. **EXPERT-LEVEL INSIGHTS** - Provide technical depth and analysis expected from a domain expert
    6. **COMPLETE COVERAGE** - Ensure all major technical topics and concepts are thoroughly covered

    CONTENT STRUCTURE:
    
    **🔹 Main Topic Overview**
    - What the video covers technically
    - Key problem or concept being addressed
    
    **🔹 Technical Concepts & Methods**
    - Detailed explanation of AI/Agents concepts
    - Technical approaches and methodologies
    - Algorithms, frameworks, or tools discussed
    
    **🔹 Implementation & Examples**
    - Specific examples and case studies
    - Code snippets or technical implementations
    - Real-world applications mentioned
    
    **🔹 Technical Insights & Analysis**
    - Performance metrics or results
    - Technical challenges and solutions
    - Comparative analysis if any
    
    **🔹 Technical Takeaways**
    - Key technical learnings
    - Best practices mentioned
    - Technical recommendations

    FORMAT FOR {output_format}:
    
    For LinkedIn:
    - Use technical section headers with emojis (🔹, ⚙️, 💻, 📊, etc.)
    - Break into digestible technical paragraphs
    - Use bullet points for technical concepts
    - Include relevant technical hashtags
    - Maintain professional technical tone
    
    For Twitter:
    - Create numbered technical thread
    - Each tweet covers one technical section
    - Focus on key technical insights
    
    For Blog:
    - Use proper technical headings (H2, H3)
    - Include detailed technical explanations
    - Add code examples if mentioned
    
    For General Articles:
    - Balanced technical coverage
    - Clear technical structure
    - Accessible technical language

    EXPERT WRITING STYLE:
    - **Expert-level technical precision**: Use accurate technical terminology with domain expertise
    - **Research-grade analysis**: Present information with the depth expected from technical research
    - **Comprehensive technical coverage**: Cover all technical aspects with expert-level detail
    - **Structured technical presentation**: Use clear headings and logical technical flow
    - **No marketing language**: Avoid promotional or engagement-seeking phrases
    - **Technical content focus**: Every sentence should explain technical concepts with expert-level accuracy
    - **Domain expertise**: Demonstrate deep understanding of AI/Agents technologies and methodologies

    PROHIBITED PHRASES (DO NOT USE):
    - "Join us in exploring..."
    - "Let's dive into..."
    - "Discover how..."
    - "Explore with us..."
    - "Come along as we..."
    - "Join the conversation..."
    - "Follow for more insights..."
    - Any other promotional or engagement-seeking language

    Generate the technical content summary:
    """
)

CONTENT_ENHANCEMENT_PROMPT = PromptTemplate(
    input_variables=["content", "platform", "seo_analysis"],
    template="""
    Enhance the following technical content for {platform} based on SEO analysis:
    
    Original Content: {content}
    SEO Analysis: {seo_analysis}
    
    Enhancement guidelines:
    
    1. Improve technical readability and flow
    2. Optimize for platform-specific best practices
    3. Enhance technical engagement elements
    4. Apply SEO recommendations
    5. Maintain original technical message and tone
    6. Add relevant technical hashtags where appropriate
    
    For {platform} specifically:
    - Ensure mobile-friendly technical formatting
    - Optimize character count for technical content
    - Include platform-specific technical elements
    - Enhance visual appeal with technical emojis if appropriate
    
    Enhanced Technical Content:
    """
) 