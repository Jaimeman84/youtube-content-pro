from typing import Optional
import ffmpeg
import whisper

class AudioProcessor:
    def __init__(self):
        self.model = whisper.load_model("base")

    def extract_audio(self, video_path: str, output_path: str) -> str:
        try:
            stream = ffmpeg.input(video_path)
            stream = ffmpeg.output(stream, output_path, acodec='libmp3lame')
            ffmpeg.run(stream, overwrite_output=True)
            return output_path
        except ffmpeg.Error as e:
            raise Exception(f"Error extracting audio: {str(e)}")

    def transcribe_audio(self, audio_path: str, language: Optional[str] = None) -> str:
        try:
            result = self.model.transcribe(audio_path, language=language)
            return result["text"]
        except Exception as e:
            raise Exception(f"Error transcribing audio: {str(e)}")
