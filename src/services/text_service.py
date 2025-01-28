import openai
from typing import Dict, List, Optional
import json

class TextProcessor:
    def __init__(self, api_key: str):
        """Initialize with OpenAI API key"""
        openai.api_key = api_key

    def _parse_json_response(self, text: str) -> Dict:
        """Helper function to safely parse JSON from OpenAI response"""
        try:
            # Try to parse as is first
            return json.loads(text)
        except json.JSONDecodeError:
            try:
                # Find the first { and last } to extract JSON
                start = text.find('{')
                end = text.rfind('}') + 1
                if start != -1 and end != 0:
                    return json.loads(text[start:end])
                raise ValueError("No JSON object found in response")
            except Exception as e:
                raise Exception(f"Failed to parse JSON response: {str(e)}")

    def generate_summary(self, text: str, max_length: int = 150) -> str:
        """Generate a summary of the text using GPT"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a content summarizer. Create a concise summary."},
                    {"role": "user", "content": f"Summarize this text in {max_length} words or less:\n{text}"}
                ],
                max_tokens=max_length * 2,  # Double the tokens to account for word-to-token ratio
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Error generating summary: {str(e)}")

    def generate_social_posts(self, video_title: str, description: str, duration: str) -> Dict:
        """Generate social media posts for different platforms"""
        try:
            prompt = f"""Create social media posts for this YouTube video. Return ONLY a JSON object with the following format:
            {{
                "twitter": "tweet text with hashtags (280 chars max)",
                "instagram": "caption with emojis and hashtags",
                "linkedin": "professional post with call to action",
                "facebook": "engaging post with video preview suggestion"
            }}

            Video Details:
            Title: {video_title}
            Description: {description}
            Duration: {duration}
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a social media expert. Create platform-specific posts. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            return self._parse_json_response(response.choices[0].message.content)
        except Exception as e:
            raise Exception(f"Error generating social posts: {str(e)}")

    def analyze_seo(self, title: str, description: str, tags: List[str]) -> Dict:
        """Analyze and suggest SEO improvements"""
        try:
            prompt = f"""Analyze this YouTube content for SEO optimization. Return ONLY a JSON object with the following format:
            {{
                "title_suggestions": ["improved title 1", "improved title 2", "improved title 3"],
                "description_improvements": "specific suggestions for description",
                "tag_suggestions": ["tag1", "tag2", "tag3", ...],
                "missing_elements": ["element1", "element2", ...]
            }}

            Content to analyze:
            Title: {title}
            Description: {description}
            Current Tags: {', '.join(tags) if tags else 'No tags'}
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an SEO expert. Provide analysis in valid JSON format only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            return self._parse_json_response(response.choices[0].message.content)
        except Exception as e:
            raise Exception(f"Error analyzing SEO: {str(e)}")

    def analyze_trending_topics(self, category: str) -> Dict:
        """Analyze trending topics in a specific category"""
        try:
            prompt = f"""Analyze trending topics for YouTube content. Return ONLY a JSON object with the following format:
            {{
                "trending_topics": ["topic1", "topic2", "topic3"],
                "content_ideas": ["idea1", "idea2", "idea3"],
                "best_practices": ["practice1", "practice2", "practice3"],
                "optimal_timing": "best posting times and frequency"
            }}

            Category: {category}
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a content strategy expert. Analyze trends and return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            return self._parse_json_response(response.choices[0].message.content)
        except Exception as e:
            raise Exception(f"Error analyzing trends: {str(e)}")

    def suggest_hashtags(self, title: str, description: str, category: str) -> List[str]:
        """
        Generate relevant hashtags for the video
        
        Args:
            title (str): Video title
            description (str): Video description
            category (str): Video category
            
        Returns:
            List[str]: List of relevant hashtags
        """
        try:
            prompt = f"""Generate exactly 15 relevant hashtags for this YouTube video.
            Important: Your response should be ONLY a comma-separated list of hashtags, nothing else.

            Video Details:
            Title: {title}
            Description: {description}
            Category: {category}

            Response Format Example:
            #YouTube, #ContentCreator, #VideoEditing, #Tutorial, #Learning

            Requirements:
            - Each hashtag must start with #
            - No spaces in hashtags
            - No quotes or special characters
            - Focus on relevant, searchable terms
            - Mix of popular and niche hashtags
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a hashtag generator. Respond only with comma-separated hashtags."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            # Get the raw response text
            hashtag_text = response.choices[0].message.content.strip()
            
            # Split by comma and clean up each hashtag
            hashtags = [tag.strip() for tag in hashtag_text.split(',')]
            
            # Ensure each hashtag starts with #
            hashtags = [tag if tag.startswith('#') else f'#{tag}' for tag in hashtags]
            
            # Remove any empty hashtags and limit to 15
            hashtags = [tag for tag in hashtags if len(tag) > 1][:15]
            
            return hashtags
            
        except Exception as e:
            raise Exception(f"Error generating hashtags: {str(e)}")

    def transcribe_video(self, text: str) -> str:
        """
        Transcribe video content using OpenAI
        
        Args:
            text (str): Raw audio transcription text
            
        Returns:
            str: Cleaned and formatted transcription
        """
        try:
            prompt = f"""Clean and format this transcription text. Return proper punctuation, paragraphs, and speaker labels if detected:

            {text}

            Format the response as regular text with proper formatting and punctuation.
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert transcriber. Format text into clean, readable transcriptions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )

            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise Exception(f"Error formatting transcription: {str(e)}")

    def extract_key_points(self, transcription: str) -> List[str]:
        """
        Extract key points from transcription
        
        Args:
            transcription (str): Video transcription
            
        Returns:
            List[str]: List of key points
        """
        try:
            prompt = f"""Extract the main key points from this transcription. 
            Return a simple list of the most important points discussed:

            {transcription}

            Return 5-7 key points, focusing on the main ideas and takeaways.
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a content analyzer. Extract key points from transcriptions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )

            points = response.choices[0].message.content.strip().split('\n')
            # Clean up points and remove empty lines
            return [p.strip('- ').strip() for p in points if p.strip()]
            
        except Exception as e:
            raise Exception(f"Error extracting key points: {str(e)}")

    def generate_video_script(self, title: str, outline: str) -> Dict:
        """Generate a video script from a title and outline"""
        try:
            prompt = f"""Create a video script. Return ONLY a JSON object with the following format:
            {{
                "intro": "hook and introduction text",
                "sections": [
                    {{"title": "section1 title", "content": "section1 content"}},
                    {{"title": "section2 title", "content": "section2 content"}}
                ],
                "outro": "call to action and closing text",
                "timestamps": [
                    {{"time": "00:00", "description": "Intro"}},
                    {{"time": "01:30", "description": "Section 1"}}
                ]
            }}

            Title: {title}
            Outline: {outline}
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a video script writer. Create engaging scripts in valid JSON format only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            return self._parse_json_response(response.choices[0].message.content)
        except Exception as e:
            raise Exception(f"Error generating video script: {str(e)}")