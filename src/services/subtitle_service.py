from typing import Dict, List
from googletrans import Translator
import whisper

class SubtitleGenerator:
    def __init__(self):
        self.model = whisper.load_model("base")
        self.translator = Translator()

    def generate_subtitles(self, audio_path: str, target_languages: List[str]) -> Dict[str, str]:
        try:
            # First get English transcription
            result = self.model.transcribe(audio_path)
            subtitles = {"en": result["text"]}
            
            # Translate to target languages
            for lang in target_languages:
                if lang != "en":
                    translation = self.translator.translate(
                        result["text"],
                        dest=lang
                    )
                    subtitles[lang] = translation.text
                    
            return subtitles
        except Exception as e:
            raise Exception(f"Error generating subtitles: {str(e)}")

    def save_subtitles(self, subtitles: Dict[str, str], output_path: str, format: str = "srt") -> Dict[str, str]:
        subtitle_files = {}
        for lang, text in subtitles.items():
            file_path = f"{output_path}/subtitles_{lang}.{format}"
            with open(file_path, "w", encoding="utf-8") as f:
                # Implementation of subtitle formatting based on format type
                pass
            subtitle_files[lang] = file_path
        return subtitle_files