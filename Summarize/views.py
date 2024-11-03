from django.http import JsonResponse
from src.Summarizer.AbstractiveSummarizer import AbstractiveSummarizer
from src.Summarizer.FrequencyBasedSummarizer import FrequencyBasedSummarizer
from src.Summarizer.LuhnSummarizer import LuhnSummarizer
from src.Translator.TranslatorService import TranslatorService
from src.YoutubeTranscript.YouTubeTranscriptFetcher import YouTubeTranscriptFetcher


def hello_world(request):
    return JsonResponse({"message": "Hello, World!"})


def get_summarized_text(request):
    youtube_video = request.GET.get('youtube_url')

    video_id = youtube_video.split("=")[1]

    choice = request.GET.get('choice')
    print(choice)
    percent = request.GET.get('percent')
    print(percent)

    translator_service = TranslatorService()
    text_fetcher = YouTubeTranscriptFetcher()

    result = text_fetcher.get_transcript(video_id)
    language = translator_service.detect_language(result)

    if language != "english":
        result = translator_service.translate_to_english(result)

    summarizer = {
        "freq-based": FrequencyBasedSummarizer(),
        "luhn-algo": LuhnSummarizer(),
        "abstractive": AbstractiveSummarizer()
    }.get(choice, FrequencyBasedSummarizer())

    summary = summarizer.summarize(result, percent)
    return JsonResponse({"summary": summary})
