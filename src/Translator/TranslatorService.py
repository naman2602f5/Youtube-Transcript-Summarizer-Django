from googletrans import Translator, constants


class TranslatorService:
    def __init__(self):
        self.translator = Translator()

    def detect_language(self, text):
        result = text.replace(">>", "").strip()
        text_to_detect = result[:50] if len(result) > 50 else result

        detection = self.translator.detect(text_to_detect)

        language = constants.LANGUAGES[detection.lang]
        return language

    def translate_to_english(self, text, max_chunk_size=1000):
        chunks = self.split_text_into_chunks(text, max_chunk_size)
        translated_chunks = [self.translator.translate(chunk, src='auto', dest='en').text for chunk in chunks]
        return ' '.join(translated_chunks)

    def split_text_into_chunks(self, text, max_chunk_size=1000):
        chunks = []
        while len(text) > max_chunk_size:
            split_index = text.rfind('.', 0, max_chunk_size) + 1
            if split_index == 0:
                split_index = max_chunk_size
            chunks.append(text[:split_index].strip())
            text = text[split_index:].strip()
        chunks.append(text)
        return chunks