import pytest
import os
import tempfile
from validators import (
    YouTubeValidator,
    TimeValidator,
    FormatValidator,
    FileValidator,
    ValidationResult,
    VideoResolution,
    VideoFormat
)

class TestYouTubeValidator:
    """Test cases for YouTube URL validation"""
    
    def test_valid_youtube_urls(self):
        valid_urls = [
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'https://youtu.be/dQw4w9WgXcQ',
            'https://youtube.com/watch?v=dQw4w9WgXcQ',
            'https://m.youtube.com/watch?v=dQw4w9WgXcQ'
        ]
        
        for url in valid_urls:
            result = YouTubeValidator.validate_url(url)
            assert result.is_valid
            assert result.value == 'dQw4w9WgXcQ'
            assert result.error_message is None
    
    def test_invalid_youtube_urls(self):
        invalid_urls = [
            'https://example.com',
            'https://youtube.com/watch',
            'https://youtube.com/watch?v=',
            'https://youtu.be/',
            'invalid_url',
            'https://youtube.com/watch?v=invalid-id-length',
            'https://youtube.com/watch?v=123$%^&*()'
        ]
        
        for url in invalid_urls:
            result = YouTubeValidator.validate_url(url)
            assert not result.is_valid
            assert result.value is None
            assert result.error_message is not None

class TestTimeValidator:
    """Test cases for time format validation"""
    
    def test_valid_timestamps(self):
        test_cases = [
            ('01:30:45', 5445),  # 1h 30m 45s
            ('00:01:30', 90),    # 1m 30s
            ('1:30:45', 5445),   # 1h 30m 45s (no leading zero)
            ('30:45', 1845),     # 30m 45s
            ('45', 45),          # 45s
            ('00:00:00', 0),     # Zero time
            ('59:59', 3599),     # Max minutes and seconds
            ('23:59:59', 86399)  # Max hours, minutes, and seconds
        ]
        
        for timestamp, expected_seconds in test_cases:
            result = TimeValidator.validate_timestamp(timestamp)
            assert result.is_valid
            assert result.value == expected_seconds
            assert result.error_message is None
    
    def test_invalid_timestamps(self):
        invalid_timestamps = [
            '25:00:00',    # Invalid hours
            '00:60:00',    # Invalid minutes
            '00:00:60',    # Invalid seconds
            'invalid',     # Invalid format
            '1:2:3',       # Invalid format
            '',           # Empty string
            '::::',       # Invalid separators
            '01:30:45:00', # Too many components
            '-01:30:45',   # Negative time
            'abc:de:fg'    # Non-numeric values
        ]
        
        for timestamp in invalid_timestamps:
            result = TimeValidator.validate_timestamp(timestamp)
            assert not result.is_valid
            assert result.error_message is not None
    
    def test_duration_validation(self):
        # Test valid durations
        valid_cases = [
            (0, 30, 60),      # 30 seconds, max 60
            (10, 20, 30),     # 10 seconds, max 30
            (0, 3600, None),  # 1 hour, no max
            (1800, 3600, 7200) # 30 minutes, max 2 hours
        ]
        
        for start, end, max_duration in valid_cases:
            result = TimeValidator.validate_duration(
                start, 
                end, 
                max_duration if max_duration is not None else float('inf')
            )
            assert result.is_valid
            assert result.value == (end - start)
            assert result.error_message is None
        
        # Test invalid durations
        invalid_cases = [
            (-1, 30, 60),     # Negative start
            (0, -30, 60),     # Negative end
            (30, 20, 60),     # End before start
            (0, 61, 60),      # Exceeds max duration
            (0, 3600, 1800)   # Exceeds max duration
        ]
        
        for start, end, max_duration in invalid_cases:
            result = TimeValidator.validate_duration(start, end, max_duration)
            assert not result.is_valid
            assert result.error_message is not None

class TestFormatValidator:
    """Test cases for format validation"""
    
    def test_valid_resolutions(self):
        valid_resolutions = [
            "360p",
            "720p",
            "1080p",
            "4K"
        ]
        
        for resolution in valid_resolutions:
            result = FormatValidator.validate_resolution(resolution)
            assert result.is_valid
            assert isinstance(result.value, VideoResolution)
            assert result.error_message is None
    
    def test_invalid_resolutions(self):
        invalid_resolutions = [
            "480p",
            "2K",
            "invalid",
            "",
            "1080",
            "720P"
        ]
        
        for resolution in invalid_resolutions:
            result = FormatValidator.validate_resolution(resolution)
            assert not result.is_valid
            assert result.error_message is not None
    
    def test_valid_video_formats(self):
        valid_formats = [
            "mp4",
            "MP4",
            "webm",
            "WEBM",
            "mkv",
            "MKV"
        ]
        
        for format in valid_formats:
            result = FormatValidator.validate_video_format(format)
            assert result.is_valid
            assert isinstance(result.value, VideoFormat)
            assert result.error_message is None
    
    def test_invalid_video_formats(self):
        invalid_formats = [
            "avi",
            "mov",
            "invalid",
            "",
            "mp3",
            "123"
        ]
        
        for format in invalid_formats:
            result = FormatValidator.validate_video_format(format)
            assert not result.is_valid
            assert result.error_message is not None