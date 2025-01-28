from typing import Optional, Dict, Any, List
from urllib.parse import urlparse, parse_qs
import re
from dataclasses import dataclass
from enum import Enum
import os

class VideoResolution(str, Enum):
    LOW = "360p"
    MEDIUM = "720p"
    HIGH = "1080p"
    ULTRA = "4K"

class VideoFormat(str, Enum):
    MP4 = "mp4"
    WEBM = "webm"
    MKV = "mkv"

@dataclass
class ValidationResult:
    """Data class to hold validation results"""
    is_valid: bool
    value: Any = None
    error_message: Optional[str] = None

class YouTubeValidator:
    """Class to handle YouTube-specific validations"""
    
    YOUTUBE_DOMAINS = {'youtube.com', 'youtu.be', 'www.youtube.com', 'm.youtube.com'}
    VIDEO_ID_PATTERN = re.compile(r'^[A-Za-z0-9_-]{11}$')
    
    @staticmethod
    def validate_url(url: str) -> ValidationResult:
        """
        Validate YouTube URL and extract video ID
        
        Args:
            url (str): YouTube URL to validate

        Returns:
            ValidationResult: Validation result with video ID if valid
        """
        try:
            parsed_url = urlparse(url)
            
            if parsed_url.netloc not in YouTubeValidator.YOUTUBE_DOMAINS:
                return ValidationResult(
                    is_valid=False,
                    error_message="Invalid YouTube domain"
                )
            
            if 'youtube.com' in parsed_url.netloc:
                query_params = parse_qs(parsed_url.query)
                video_id = query_params.get('v', [None])[0]
            else:  # youtu.be
                video_id = parsed_url.path.lstrip('/')
            
            if not video_id or not YouTubeValidator.VIDEO_ID_PATTERN.match(video_id):
                return ValidationResult(
                    is_valid=False,
                    error_message="Invalid video ID format"
                )
            
            return ValidationResult(is_valid=True, value=video_id)
            
        except Exception as e:
            return ValidationResult(
                is_valid=False,
                error_message=f"URL parsing error: {str(e)}"
            )

class TimeValidator:
    """Class to handle time-related validations"""
    
    TIME_FORMATS = {
        'HH:MM:SS': re.compile(r'^(\d{1,2}):([0-5]\d):([0-5]\d)$'),
        'MM:SS': re.compile(r'^([0-5]?\d):([0-5]\d)$'),
        'SS': re.compile(r'^([0-5]?\d)$')
    }
    
    @staticmethod
    def validate_timestamp(timestamp: str) -> ValidationResult:
        """
        Validate timestamp in various formats and convert to seconds
        
        Args:
            timestamp (str): Timestamp in format HH:MM:SS, MM:SS, or SS

        Returns:
            ValidationResult: Validation result with seconds if valid
        """
        timestamp = timestamp.strip()
        
        for format_name, pattern in TimeValidator.TIME_FORMATS.items():
            match = pattern.match(timestamp)
            if match:
                try:
                    groups = match.groups()
                    if format_name == 'HH:MM:SS':
                        hours, minutes, seconds = map(int, groups)
                        total_seconds = hours * 3600 + minutes * 60 + seconds
                    elif format_name == 'MM:SS':
                        minutes, seconds = map(int, groups)
                        total_seconds = minutes * 60 + seconds
                    else:  # SS
                        total_seconds = int(groups[0])
                    
                    return ValidationResult(is_valid=True, value=total_seconds)
                except ValueError as e:
                    return ValidationResult(
                        is_valid=False,
                        error_message=f"Invalid time values: {str(e)}"
                    )
        
        return ValidationResult(
            is_valid=False,
            error_message="Invalid timestamp format"
        )
    
    @staticmethod
    def validate_duration(start: float, end: float, max_duration: float = float('inf')) -> ValidationResult:
        """
        Validate video duration constraints
        
        Args:
            start (float): Start time in seconds
            end (float): End time in seconds
            max_duration (float): Maximum allowed duration in seconds
        """
        try:
            if start < 0 or end < 0:
                return ValidationResult(
                    is_valid=False,
                    error_message="Timestamps cannot be negative"
                )
            
            if start >= end:
                return ValidationResult(
                    is_valid=False,
                    error_message="Start time must be before end time"
                )
            
            duration = end - start
            if duration > max_duration:
                return ValidationResult(
                    is_valid=False,
                    error_message=f"Duration exceeds maximum allowed ({max_duration} seconds)"
                )
            
            return ValidationResult(is_valid=True, value=duration)
            
        except Exception as e:
            return ValidationResult(
                is_valid=False,
                error_message=f"Duration validation error: {str(e)}"
            )

class FormatValidator:
    """Class to handle format-related validations"""
    
    @staticmethod
    def validate_resolution(resolution: str) -> ValidationResult:
        """Validate video resolution format"""
        try:
            resolution_enum = VideoResolution(resolution)
            return ValidationResult(is_valid=True, value=resolution_enum)
        except ValueError:
            return ValidationResult(
                is_valid=False,
                error_message=f"Invalid resolution. Supported values: {[r.value for r in VideoResolution]}"
            )
    
    @staticmethod
    def validate_video_format(format: str) -> ValidationResult:
        """Validate video file format"""
        try:
            format_enum = VideoFormat(format.lower())
            return ValidationResult(is_valid=True, value=format_enum)
        except ValueError:
            return ValidationResult(
                is_valid=False,
                error_message=f"Invalid format. Supported formats: {[f.value for f in VideoFormat]}"
            )

class FileValidator:
    """Class to handle file-related validations"""
    
    @staticmethod
    def validate_output_path(path: str) -> ValidationResult:
        """Validate output file path"""
        try:
            directory = os.path.dirname(path)
            if directory and not os.path.exists(directory):
                try:
                    os.makedirs(directory)
                except Exception as e:
                    return ValidationResult(
                        is_valid=False,
                        error_message=f"Cannot create directory: {str(e)}"
                    )
            
            try:
                with open(path, 'a'): pass
                os.remove(path)  # Clean up test file
                return ValidationResult(is_valid=True, value=path)
            except Exception as e:
                return ValidationResult(
                    is_valid=False,
                    error_message=f"Cannot write to file: {str(e)}"
                )
                
        except Exception as e:
            return ValidationResult(
                is_valid=False,
                error_message=f"Path validation error: {str(e)}"
            )
    
    @staticmethod
    def validate_file_size(file_size: int, max_size_mb: float) -> ValidationResult:
        """
        Validate file size against maximum allowed size
        
        Args:
            file_size (int): File size in bytes
            max_size_mb (float): Maximum allowed size in megabytes
        """
        max_size_bytes = max_size_mb * 1024 * 1024
        
        if file_size <= 0:
            return ValidationResult(
                is_valid=False,
                error_message="Invalid file size"
            )
        
        if file_size > max_size_bytes:
            return ValidationResult(
                is_valid=False,
                error_message=f"File size exceeds maximum allowed size of {max_size_mb}MB"
            )
        
        return ValidationResult(is_valid=True, value=file_size)