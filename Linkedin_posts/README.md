# YouTube Multi-Agent Content Workflow

Transform YouTube videos into engaging, platform-optimized content using AI-powered multi-agent workflows.

## 🎯 What This Project Does

This project takes a **YouTube video URL** as input and automatically generates **LinkedIn posts** (and other platform content) using three specialized AI agents working together.

### Simple Workflow:
```
YouTube URL → Extract Transcript → Generate Title → Create Content → LinkedIn Post
```

## 🚀 Features

### Three Specialized AI Agents:
- **📝 Transcript Agent**: Extracts and cleans YouTube video transcripts
- **🎯 Title Agent**: Generates engaging, clickable titles with trend analysis  
- **📄 Content Agent**: Creates structured, platform-optimized content

### 🎨 Supported Platforms:
- **LinkedIn**: Posts with hashtags and engagement hooks
- **Blog**: Articles with proper SEO structure and headings
- **Twitter**: Optimized threads with character limits
- **General Articles**: Comprehensive formatting and structure

### 🛠️ Advanced Capabilities:
- SEO analysis and optimization recommendations
- Content structuring for different platforms
- Trend-based title generation using web search
- Bulk processing for multiple videos
- Comprehensive error handling and logging

## 🏗️ Project Structure

```
Linkedin_posts/
├── src/
│   ├── agents/           # 🤖 Three AI agents
│   │   ├── transcript_agent.py    # Extracts YouTube transcripts
│   │   ├── title_agent.py         # Generates engaging titles
│   │   ├── content_agent.py       # Creates platform content
│   │   └── base_agents.py         # Base agent class
│   ├── tools/            # 🛠️ LangChain tools
│   │   ├── youtube_tools.py       # YouTube transcript extraction
│   │   ├── content_tools.py       # Content analysis tools
│   │   └── seo_tools.py           # SEO analysis tools
│   ├── workflows/        # 🔄 LangGraph workflow
│   │   └── youtube_workflow.py    # Main workflow orchestration
│   ├── models/           # 📋 Data models
│   │   └── state.py              # Agent state definition
│   └── config/           # ⚙️ Configuration
│       └── settings.py           # App settings
├── api/                  # 🌐 FastAPI REST API
│   ├── main.py                   # API server
│   └── routes/
│       ├── workflow.py           # Main API endpoints
│       └── health.py             # Health checks
├── prompts/              # 💬 LLM prompts
│   ├── transcript_prompts.py     # Transcript cleaning prompts
│   ├── title_prompts.py          # Title generation prompts
│   └── content_prompts.py        # Content creation prompts
├── utils/                # 🔧 Utility functions
│   ├── logger.py                 # Logging setup
│   ├── exceptions.py             # Custom exceptions
│   ├── helpers.py                # Helper functions
│   └── validators.py             # Input validation
└── tests/                # 🧪 Test suite
```

## 🔄 How the LinkedIn Posts Workflow Works

### Step-by-Step Process:

1. **📥 Input**: User provides YouTube URL
   ```
   https://www.youtube.com/watch?v=VIDEO_ID
   ```

2. **📝 Transcript Extraction** (TranscriptAgent)
   - Extracts raw transcript from YouTube
   - Cleans and formats the text
   - Removes filler words and timestamps

3. **🎯 Title Generation** (TitleAgent)
   - Analyzes transcript for key themes
   - Searches for trending topics
   - Generates engaging, LinkedIn-optimized title

4. **📄 Content Creation** (ContentAgent)
   - Creates LinkedIn post from transcript and title
   - Adds professional formatting
   - Includes hashtags and engagement hooks
   - Performs SEO analysis

5. **📤 Output**: Ready-to-post LinkedIn content
   ```
   🚀 Just discovered some incredible AI insights...
   
   ✅ Key takeaways:
   • Point 1
   • Point 2
   • Point 3
   
   What's your experience with this? Share below! 👇
   
   #AI #Technology #Innovation #LinkedIn
   ```

### 🤖 Agent Details:

#### **TranscriptAgent**
- **Tools**: YouTube transcript API, metadata extraction
- **Output**: Clean, formatted transcript text
- **Features**: Removes filler words, fixes grammar, maintains meaning

#### **TitleAgent**
- **Tools**: Content analysis, web search for trends
- **Output**: Engaging, platform-optimized title
- **Features**: Keyword analysis, trend integration, platform-specific optimization

#### **ContentAgent**
- **Tools**: Content structure analysis, SEO analysis
- **Output**: Platform-ready content with formatting
- **Features**: Professional tone, engagement hooks, hashtag optimization

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/youtube-agent-workflow
cd youtube-agent-workflow

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Setup

```bash
# Create .env file
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

### 3. Run the Application

```bash
# Start the API server
python api/main.py
```

### 4. Generate Your First LinkedIn Post

```bash
curl -X POST "http://localhost:8000/workflow/linkedin-post" \
     -H "Content-Type: application/json" \
     -d '{
       "url": "https://www.youtube.com/watch?v=YOUR_VIDEO_ID",
       "output_format": "linkedin",
       "language": "en"
     }'
```

## 📡 API Endpoints

### LinkedIn-Specific Endpoints:
- `POST /workflow/linkedin-post` - Generate single LinkedIn post
- `POST /workflow/linkedin-bulk` - Generate multiple LinkedIn posts
- `GET /workflow/linkedin-preview` - Preview LinkedIn formatting

### General Endpoints:
- `POST /workflow/process-video` - Process single YouTube video
- `POST /workflow/process-bulk` - Process multiple videos
- `GET /workflow/workflow-info` - Get workflow details
- `GET /health` - Health check

### Example Request:
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "output_format": "linkedin",
  "language": "en"
}
```

### Example Response:
```json
{
  "transcript": "Clean transcript text...",
  "title": "5 Game-Changing AI Insights That Will Transform Your Business",
  "content": "🚀 Just discovered some incredible AI insights...\n\n✅ Key takeaways:\n• Insight 1\n• Insight 2\n• Insight 3\n\nWhat's your experience with this? Share below! 👇\n\n#AI #Technology #Innovation #LinkedIn",
  "metadata": {
    "video_id": "dQw4w9WgXcQ",
    "processed_at": "2025-01-21T10:30:00Z",
    "workflow_version": "2.0.0"
  },
  "seo_analysis": {
    "readability_score": 85.5,
    "word_count": 420,
    "seo_score": 92,
    "recommendations": ["Add more hashtags", "Include call-to-action"]
  }
}
```

## 🎯 LinkedIn-Specific Features

### Content Optimization:
- **Character Limit**: Optimized for LinkedIn's 3000 character limit
- **Professional Tone**: Business-focused with personality
- **Engagement Hooks**: Questions, numbered lists, story elements
- **Hashtag Optimization**: Relevant industry hashtags
- **Call-to-Action**: Professional CTAs for engagement

### Formatting Features:
- **Mobile-Friendly**: Short paragraphs and bullet points
- **Visual Appeal**: Strategic emoji usage
- **Professional Structure**: Clear sections and flow
- **SEO Elements**: Keywords and meta descriptions

## 🐳 Docker Deployment

```bash
# Build and run with Docker
docker-compose up --build -d
```

## ⚙️ Configuration

Key environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key (required) | - |
| `OPENAI_MODEL` | OpenAI model to use | gpt-3.5-turbo |
| `PORT` | Server port | 8000 |
| `LOG_LEVEL` | Logging level | INFO |

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_agents.py -v
```

## 📊 Monitoring and Logging

- Comprehensive logging with structured format
- Health check endpoint for monitoring
- Request/response tracking
- Error handling with detailed messages

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📖 [Documentation](https://github.com/yourusername/youtube-agent-workflow#readme)
- 🐛 [Issue Tracker](https://github.com/yourusername/youtube-agent-workflow/issues)
- 💬 [Discussions](https://github.com/yourusername/youtube-agent-workflow/discussions)

## 🎯 Roadmap

- [ ] Support for more platforms (Instagram, TikTok)
- [ ] Advanced SEO optimization
- [ ] Content scheduling integration
- [ ] Multi-language support expansion
- [ ] Redis caching for performance
- [ ] Webhook support for integrations
- [ ] Analytics and reporting dashboard