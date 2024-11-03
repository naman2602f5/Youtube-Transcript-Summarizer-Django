from src.Summarizer.BaseSummarizer import BaseSummarizer
from transformers import pipeline
import re


class AbstractiveSummarizer(BaseSummarizer):
    def summarize(self, text, percent):
        chunks = self._create_chunks(text)
        summarizer = pipeline('summarization')
        summarized_text = summarizer(chunks)
        summary = ' '.join([summ['summary_text'] for summ in summarized_text])
        return summary

    def _create_chunks(self, result, max_chunk=500):
        result = re.sub(r'\s+', ' ', result)
        result = result.replace('.', '.<eos>')
        result = result.replace('?', '?<eos>')
        result = result.replace('!', '!<eos>')
        sentences = result.split('<eos>')
        current_chunk = 0
        chunks = []
        for sentence in sentences:
            if len(chunks) == current_chunk + 1:
                if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
                    chunks[current_chunk].extend(sentence.split(' '))
                else:
                    current_chunk += 1
                    chunks.append(sentence.split(' '))
            else:
                print(current_chunk)
                chunks.append(sentence.split(' '))

        for chunk_id in range(len(chunks)):
            chunks[chunk_id] = ' '.join(chunks[chunk_id])
        print(len(chunks))
        return chunks