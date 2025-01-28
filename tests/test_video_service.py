import pytest
from src.services.video_service import VideoProcessor
from unittest.mock import Mock, patch
import ffmpeg

def test_clip_video():
    with patch('ffmpeg.input') as mock_input:
        with patch('ffmpeg.output') as mock_output:
            with patch('ffmpeg.run') as mock_run:
                processor = VideoProcessor()
                result = processor.clip_video('input.mp4', 0, 10, 'output.mp4')
                
                assert result == 'output.mp4'
                mock_input.assert_called_once_with('input.mp4')

def test_format_for_shorts():
    with patch('ffmpeg.input') as mock_input:
        with patch('ffmpeg.filter') as mock_filter:
            with patch('ffmpeg.output') as mock_output:
                with patch('ffmpeg.run') as mock_run:
                    processor = VideoProcessor()
                    result = processor.format_for_shorts('input.mp4', 'output.mp4')
                    
                    assert result == 'output.mp4'
         