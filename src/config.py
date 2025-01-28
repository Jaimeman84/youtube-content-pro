import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # API Keys
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # File paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DOWNLOAD_PATH = os.path.join(BASE_DIR, "downloads")
    TEMP_PATH = os.path.join(BASE_DIR, "temp")
    
    # Create directories if they don't exist
    os.makedirs(DOWNLOAD_PATH, exist_ok=True)
    os.makedirs(TEMP_PATH, exist_ok=True)
    
    # Video processing settings
    MAX_VIDEO_SIZE_MB = 500
    SUPPORTED_RESOLUTIONS = ["360p", "720p", "1080p"]
    SHORTS_DIMENSIONS = {
        "width": 1080,
        "height": 1920
    }