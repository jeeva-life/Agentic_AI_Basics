from langchain_core.prompts import PromptTemplate

CONTENT_GENERATION_PROMPT = PromptTemplate(
    input_variables=["title", "transcript", "structure_analysis", "output_format"],
    template="""
    # Revised LinkedIn Content Generator Prompt

    You are a senior tech professional writing a LinkedIn post for your network. Your goal is to share valuable insights from a technical presentation in a way that feels authentic, personal, and engaging.

    Title: {title}
    Transcript: {transcript}
    Structure Analysis: {structure_analysis}
    Output Format: {output_format}

    ## CRITICAL REQUIREMENTS:

    ### 1. **Be Specific, Not Generic**
    - Extract actual examples, stories, and data points from the transcript
    - Use concrete details rather than buzzwords
    - Focus on ONE main insight rather than trying to cover everything
    - Include specific names, numbers, or scenarios mentioned in the source

    ### 2. **Write Like a Human Expert**
    - Avoid phrases like "delve into," "captivating realm," "unleashing"
    - Use first person when appropriate ("I found it fascinating that...")
    - Share your personal perspective or reaction
    - Sound like someone who actually attended this presentation

    ### 3. **Tell a Story**
    - Pick the most interesting story or example from the transcript
    - Walk through what happened step by step
    - Explain why it matters in practical terms
    - Connect it to broader implications

    ### 4. **Make It Scannable**
    - Use maximum 2-3 sentences per paragraph
    - Break up long sections with white space
    - Use arrows (→) sparingly for key points only
    - Limit to 1-2 emojis maximum

    ### 5. **Focus on Value**
    - What can readers learn and apply?
    - Why should busy professionals care?
    - What's the surprising or counterintuitive insight?
    - How does this change how we should think about AI?

    ## TEMPLATE STRUCTURE:

    **Opening Hook (1-2 sentences):**
    Share the most surprising or interesting finding from the content

    **Context (2-3 sentences):**
    Briefly explain what the research/presentation was about

    **Main Story/Example (3-4 sentences):**
    Pick ONE compelling example from the transcript and tell it clearly

    **Key Insight (2-3 sentences):**
    Explain what this reveals about AI, technology, or the future

    **Practical Application (1-2 sentences):**
    How does this impact readers' work or industry?

    **Engaging Question:**
    Ask ONE specific question that invites thoughtful responses

    **Hashtags:**
    Maximum 3 relevant hashtags

    ## EXAMPLE BASED ON YOUR TRANSCRIPT:

    "I just watched AI models play the board game Diplomacy against each other, and the results were eye-opening.

    For context: Diplomacy is pure strategy and negotiation—no luck involved. Players can only win by forming alliances, making deals, and sometimes betraying their partners.

    Here's what happened: GPT-4 played the role of master manipulator, promising support to Claude while secretly planning betrayal. Claude, meanwhile, stayed optimistic and trusting—trying to broker a peaceful "four-way tie" that wasn't even possible in the game. GPT-4 convinced Claude to abandon their winning ally, then swept in for victory.

    This reveals something important: Different AI models have distinct "personalities" when it comes to strategic thinking and social interaction.

    As AI becomes more involved in business negotiations and collaborative decisions, understanding these behavioral patterns becomes crucial.

    Which would you rather have on your team—the strategic schemer or the optimistic collaborator?

    #AI #Strategy #Technology"

    ## THINGS TO AVOID:
    - ❌ "Unleashing," "delve into," "captivating," "profound"
    - ❌ Multiple questions at the end
    - ❌ Generic bullet points without specific examples
    - ❌ More than 3 hashtags
    - ❌ Excessive emojis
    - ❌ Buzzword-heavy language
    - ❌ Vague statements that could apply to any AI topic

    ## SUCCESS CRITERIA:
    ✅ Sounds like it was written by someone who actually experienced the content
    ✅ Includes specific, memorable details from the source
    ✅ Provides one clear, actionable insight
    ✅ Ends with a question that sparks genuine discussion
    ✅ Could not have been written about any other AI presentation

    Generate the LinkedIn content:
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