import os
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import openai
from typing import Dict, List

class VideoProcessor:
    """Class for handling video processing operations"""
    
    def __init__(self, api_key: str = None, download_path: str = "downloads"):
        """
        Initialize VideoProcessor
        
        Args:
            api_key (str): OpenAI API key for content generation
            download_path (str): Path for downloading videos
        """
        if api_key:
            openai.api_key = api_key
        self.download_path = download_path
        self._ensure_directories()

    def _ensure_directories(self):
        """Create necessary directories"""
        os.makedirs(self.download_path, exist_ok=True)

    def _extract_video_id(self, url: str) -> str:
        """Extract video ID from YouTube URL"""
        try:
            if 'youtu.be' in url:
                return url.split('/')[-1].split('?')[0]
            else:
                parsed_url = urlparse(url)
                if 'youtube.com' in parsed_url.netloc:
                    return parse_qs(parsed_url.query)['v'][0]
        except Exception:
            pass
        return None

    def get_video_transcript(self, video_url: str) -> str:
        """Get transcript from YouTube video"""
        try:
            video_id = self._extract_video_id(video_url)
            if not video_id:
                raise ValueError("Could not extract video ID from URL")
            
            # Get transcript
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            
            # Format transcript as continuous text
            full_transcript = " ".join(entry['text'] for entry in transcript_list)
            
            # Add download button for transcript
            st.download_button(
                "Download Transcript",
                full_transcript,
                file_name=f"transcript_{video_id}.txt",
                mime="text/plain"
            )
            
            return full_transcript

        except Exception as e:
            raise Exception(f"Transcript error: {str(e)}")

    def generate_social_posts(self, video_url: str, transcript: str, target_platforms: List[str]) -> Dict:
        """Generate social media posts based on video content"""
        try:
            if not openai.api_key:
                raise ValueError("OpenAI API key not set. Please check your .env file.")
            
            video_id = self._extract_video_id(video_url)
            video_link = f"https://youtu.be/{video_id}"

            # Prepare platform-specific prompts
            platform_specs = {
                "Twitter": {
                    "max_length": 280,
                    "style": "engaging and concise, with relevant hashtags",
                },
                "Instagram": {
                    "max_length": 2200,
                    "style": "visual and engaging, with emojis and hashtags",
                },
                "LinkedIn": {
                    "max_length": 3000,
                    "style": "professional and insightful, with industry-relevant points",
                },
                "Facebook": {
                    "max_length": 63206,
                    "style": "conversational and engaging, encouraging discussion",
                }
            }
            
            # Generate hashtags
            hashtag_prompt = f"""Based on this YouTube video content, generate 5-7 relevant and trending hashtags:
            Content Summary: {transcript[:500]}...
            
            Format: Return only the hashtags, separated by spaces, without numbers or explanations.
            """
            
            hashtag_response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a social media expert focusing on YouTube content promotion."},
                    {"role": "user", "content": hashtag_prompt}
                ],
                temperature=0.7
            )
            
            hashtags = hashtag_response.choices[0].message.content.strip()
            posts = {}
            
            # Generate posts for each platform
            for platform in target_platforms:
                if platform not in platform_specs:
                    continue
                    
                spec = platform_specs[platform]
                prompt = f"""Create an engaging {platform} post promoting this YouTube video:
                Content Summary: {transcript[:500]}...
                Video Link: {video_link}
                
                Requirements:
                - Maximum length: {spec['max_length']} characters
                - Style: {spec['style']}
                - Include a strong hook
                - Include the video link
                - Include a call to action to watch the video
                - Use these hashtags appropriately: {hashtags}
                - For Instagram/Twitter, put the link at the end
                
                Format: Return only the post content, ready to use.
                """
                
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a social media expert focusing on YouTube content promotion."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                
                posts[platform] = response.choices[0].message.content.strip()
            
            return {
                'posts': posts,
                'hashtags': hashtags
            }

        except Exception as e:
            raise Exception(f"Error generating social media content: {str(e)}")