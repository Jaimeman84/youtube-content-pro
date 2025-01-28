import pytest
from src.services.audio_service import AudioProcessor
from unittest.mock import Mock, patch
import ffmpeg

def test_extract_audio():
    with patch('ffmpeg.input') as mock_input:
        with patch('ffmpeg.output') as mock_output:
            with patch('ffmpeg.run') as mock_run:
                processor = AudioProcessor()
                result = processor.extract_audio('test.mp4', 'test.mp3')
                
                assert result == 'test.mp3'
                mock_input.assert_called_once_with('test.mp4')
                mock_run.assert_called_once()

def test_extract_audio_error():
    with patch('ffmpeg.input') as mock_input:
        mock_input.side_effect = ffmpeg.Error('Test error')
        
        processor = AudioProcessor()
        with pytest.raises(Exception) as exc_info:
            processor.extract_audio('test.mp4', 'test.mp3')
        
        assert 'Error extracting audio' in str(exc_info.value)
