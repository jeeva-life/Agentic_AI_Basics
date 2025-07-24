"""Sample data for testing the YouTube Agent Workflow"""

SAMPLE_YOUTUBE_URLS = [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://youtu.be/dQw4w9WgXcQ", 
    "https://www.youtube.com/embed/dQw4w9WgXcQ"
]

SAMPLE_TRANSCRIPT = """
Welcome to this comprehensive tutorial about artificial intelligence and machine learning.
In this video, we'll explore the fundamental concepts that drive modern AI systems.
We'll discuss neural networks, deep learning, and their practical applications in business.
You'll learn about data preprocessing, model training, and deployment strategies.
We'll also cover the latest trends in AI including large language models and generative AI.
By the end of this video, you'll have a solid understanding of AI basics and how to apply them.
This knowledge will help you make informed decisions about implementing AI in your projects.
"""

SAMPLE_METADATA = {
    "video_id": "dQw4w9WgXcQ",
    "processed_at": "2025-01-21T10:30:00Z",
    "transcript_length": 612,
    "workflow_version": "2.0.0"
}

SAMPLE_TITLE = "5 Game-Changing AI Insights That Will Transform Your Business in 2025"

SAMPLE_LINKEDIN_CONTENT = """
🚀 Just discovered some incredible AI insights that are reshaping the business landscape!

Here are the key takeaways from my latest deep dive:

✅ AI automation is becoming mainstream - 73% of companies are already implementing it
✅ Data preprocessing is still the most critical step (garbage in = garbage out)
✅ Large language models are democratizing AI access for small businesses
✅ The ROI on AI projects averages 300% when implemented correctly
✅ Human-AI collaboration beats pure automation in most scenarios

The most surprising finding? Companies that start small and scale gradually see 40% better success rates than those attempting massive AI overhauls.

What's your experience with AI implementation? Have you seen similar results?

#AI #MachineLearning #BusinessTransformation #Innovation #Technology #DigitalTransformation
"""

SAMPLE_SEO_ANALYSIS = {
    "word_count": 145,
    "readability_score": 78.5,
    "seo_score": 85,
    "top_keywords": [
        {"word": "ai", "frequency": 8, "density": 5.5},
        {"word": "business", "frequency": 4, "density": 2.8},
        {"word": "companies", "frequency": 3, "density": 2.1}
    ],
    "recommendations": [
        "Add more internal links",
        "Include more long-tail keywords",
        "Optimize meta description"
    ]
}

SAMPLE_WORKFLOW_RESPONSE = {
    "transcript": SAMPLE_TRANSCRIPT,
    "title": SAMPLE_TITLE,
    "content": SAMPLE_LINKEDIN_CONTENT,
    "metadata": SAMPLE_METADATA,
    "seo_analysis": SAMPLE_SEO_ANALYSIS
}
