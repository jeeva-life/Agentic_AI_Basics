from langchain_core.prompts import PromptTemplate

TRANSCRIPT_ANALYSIS_PROMPT = PromptTemplate(
    input_variables=["transcript"],
    template="""
    Analyze the following YouTube video transcript and extract key insights:
    
    Transcript: {transcript}
    
    Please provide:
    1. Main topics discussed
    2. Key insights and takeaways
    3. Important quotes or statements
    4. Overall tone and style
    
    Analysis:
    """
)

TRANSCRIPT_CLEANUP_PROMPT = PromptTemplate(
    input_variables=["transcript"],
    template="""
    Clean and format the following YouTube video transcript for content generation:
    
    Raw Transcript: {transcript}
    
    Please:
    1. Remove filler words (um, uh, like, you know)
    2. Fix grammar and punctuation
    3. Break into clear sentences and paragraphs
    4. Remove speaker labels and timestamps
    5. Maintain the original meaning and flow
    6. Make it readable and professional
    
    Cleaned Transcript:
    """
) 