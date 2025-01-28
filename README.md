# YouTube Content Pro

A Streamlit application for analyzing YouTube videos and generating social media content.

## Features
- Get instant video transcripts with statistics
  - Word count and estimated duration
  - Download transcripts as text files
- Generate social media content
  - Platform-specific posts for Twitter, Instagram, LinkedIn, and Facebook
  - Trending hashtag suggestions
  - Customized content length and style per platform

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/youtube-content-pro.git
cd youtube-content-pro
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
Create a `.env` file in the root directory with:
```env
# API Keys
OPENAI_API_KEY=your_openai_api_key
```

5. Run the application
```bash
streamlit run src/main.py
```

## Usage

1. Enter a YouTube URL in the input field
2. Choose between:
   - **Get Transcript**: View and download video transcripts with statistics
   - **Social Media**: Generate platform-specific posts and hashtags

### Transcript Features
- View complete video transcript
- See word count and estimated duration
- Download transcript as text file
- View speaking rate statistics

### Social Media Features
- Select target platforms
- Generate customized posts for each platform
- Get trending hashtags based on video content
- Preview posts in expandable sections

## Testing
```bash
pytest tests/
```

## Contributing
1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License
MIT License