import pytest
from src.services.text_service import TextProcessor
from unittest.mock import Mock
import pytest
from src.services.youtube_service import YouTubeService
from unittest.mock import Mock, patch

def test_get_video_info():
    with patch('googleapiclient.discovery.build') as mock_build:
        mock_youtube = Mock()
        mock_build.return_value = mock_youtube
        
        mock_response = {
            'items': [{
                'id': 'test_id',
                'snippet': {'title': 'Test Video'}
            }]
        }
        
        mock_youtube.videos().list().execute.return_value = mock_response
        
        service = YouTubeService('dummy_api_key')
        result = service.get_video_info('https://youtube.com/watch?v=test_id')
        
        assert result['snippet']['title'] == 'Test Video'
