from typing import Dict, Optional, List
import yt_dlp
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re
import os
import time

class YouTubeService:
    """Service for interacting with YouTube API and downloading videos"""
    
    def __init__(self, api_key: str, download_path: str = "downloads"):
        """Initialize the YouTube service"""
        try:
            self.youtube = build('youtube', 'v3', developerKey=api_key)
            self.download_path = download_path
            os.makedirs(download_path, exist_ok=True)
        except Exception as e:
            raise Exception(f"Failed to initialize YouTube service: {str(e)}")

    def extract_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from various YouTube URL formats"""
        patterns = [
            r'(?:v=|/v/|^v/|youtu\.be/|/embed/|/e/|watch\?v%3D|watch\?feature=player_embedded&v=)([^#\&\?\n/<>"\']*)',
            r'(?:youtu\.be/|youtube\.com/(?:embed/|v/|watch\?v=|watch\?.+&v=))([^#\&\?\n/<>"\']*)',
            r'^[A-Za-z0-9_-]{11}$'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                video_id = match.group(1)
                if len(video_id) == 11:
                    return video_id
        return None

    def get_video_info(self, video_url: str) -> Dict:
        """Get video information using YouTube Data API"""
        try:
            video_id = self.extract_video_id(video_url)
            if not video_id:
                raise ValueError("Could not extract valid video ID from URL")

            request = self.youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=video_id
            )
            response = request.execute()

            if not response.get('items'):
                raise ValueError(f"No video found with ID: {video_id}")

            return response['items'][0]

        except HttpError as e:
            error_details = str(e) if hasattr(e, 'content') else "Unknown API error"
            raise Exception(f"YouTube API error: {error_details}")
        except Exception as e:
            raise Exception(f"Error getting video info: {str(e)}")

    def download_video(self, video_url: str, resolution: str = "720p") -> str:
        """Download YouTube video using yt-dlp"""
        try:
            # Extract video ID for filename
            video_id = self.extract_video_id(video_url)
            if not video_id:
                raise ValueError("Could not extract video ID")

            # Convert resolution to format height
            height = int(resolution.lower().replace('p', ''))
            
            # Create a temporary filename based on video ID
            temp_filename = f"video_{video_id}.mp4"
            output_template = os.path.join(self.download_path, temp_filename)

            # Configure yt-dlp options
            ydl_opts = {
                'format': f'bestvideo[height<={height}][ext=mp4]+bestaudio[ext=m4a]/best[height<={height}][ext=mp4]/best[ext=mp4]',
                'outtmpl': output_template,
                'merge_output_format': 'mp4',
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
                'ignoreerrors': True
            }

            # Download the video
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])

            # Verify file exists and return the path
            if os.path.exists(output_template):
                return output_template

            # If the exact filename doesn't exist, look for any file with the video ID
            files = os.listdir(self.download_path)
            for file in files:
                if video_id in file and file.endswith('.mp4'):
                    old_path = os.path.join(self.download_path, file)
                    new_path = output_template
                    if old_path != new_path:
                        os.rename(old_path, new_path)
                    return new_path

            raise Exception("Could not locate downloaded video file")

        except Exception as e:
            raise Exception(f"Error downloading video: {str(e)}")

    def get_available_resolutions(self, video_url: str) -> List[str]:
        """Get list of available resolutions for a video"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                formats = info.get('formats', [])
                
                resolutions = set()
                for f in formats:
                    height = f.get('height')
                    if height and f.get('ext') == 'mp4':
                        resolutions.add(f"{height}p")
                
                return sorted(list(resolutions), 
                            key=lambda x: int(x.replace('p', '')))
                            
        except Exception as e:
            raise Exception(f"Error getting available resolutions: {str(e)}")

    def cleanup_old_files(self, max_age_hours: int = 24):
        """Clean up old downloaded files"""
        try:
            current_time = time.time()
            for filename in os.listdir(self.download_path):
                filepath = os.path.join(self.download_path, filename)
                if os.path.isfile(filepath):
                    file_age = current_time - os.path.getctime(filepath)
                    if file_age > (max_age_hours * 3600):
                        os.remove(filepath)
        except Exception as e:
            print(f"Error cleaning up files: {str(e)}")