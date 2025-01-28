from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class VideoMetadata:
    video_id: str
    title: str
    description: str
    channel_id: str
    channel_title: str
    published_at: datetime
    tags: List[str]
    duration: str
    view_count: int
    like_count: Optional[int]
    comment_count: Optional[int]

@dataclass
class ProcessingOptions:
    resolution: str
    start_time: Optional[float]
    end_time: Optional[float]
    format_vertical: bool
    target_languages: List[str]

@dataclass
class ProcessingResult:
    success: bool
    output_path: Optional[str]
    error_message: Optional[str]
    metadata: Optional[dict]