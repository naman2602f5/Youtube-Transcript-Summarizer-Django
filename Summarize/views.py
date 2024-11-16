from django.http import JsonResponse
from django.views import View
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from .models import YouTubeVideo, SummarizationResult, TranslationRecord
from src.Summarizer.AbstractiveSummarizer import AbstractiveSummarizer
from src.Summarizer.FrequencyBasedSummarizer import FrequencyBasedSummarizer
from src.Summarizer.LuhnSummarizer import LuhnSummarizer
from src.Translator.TranslatorService import TranslatorService
from src.YoutubeTranscript.YouTubeTranscriptFetcher import YouTubeTranscriptFetcher


class FetchAndStoreVideoView(View):
    def get(self, request):
        youtube_video = request.GET.get('youtube_url')
        if not youtube_video:
            return JsonResponse({"error": "youtube_url parameter is required"}, status=400)

        video_id = youtube_video.split("=")[1]

        text_fetcher = YouTubeTranscriptFetcher()
        translator_service = TranslatorService()

        transcript = text_fetcher.get_transcript(video_id)
        language = translator_service.detect_language(transcript)

        # Translate if necessary
        if language != "english":
            translated_text = translator_service.translate_to_english(transcript)
        else:
            translated_text = transcript

        # Save video details
        video, created = YouTubeVideo.objects.get_or_create(
            video_id=video_id,
            defaults={
                'youtube_url': youtube_video,
                'transcript': translated_text,
                'language': language
            }
        )

        return JsonResponse({"message": "Video data fetched and stored successfully", "created": created})


class SummarizeTextView(View):
    def get(self, request):
        video_id = request.GET.get('video_id')
        choice = request.GET.get('choice', 'freq-based')
        percent = (request.GET.get('percent', 20))

        video = get_object_or_404(YouTubeVideo, video_id=video_id)

        # Select summarizer
        summarizer = {
            "freq-based": FrequencyBasedSummarizer(),
            "luhn-algo": LuhnSummarizer(),
            "abstractive": AbstractiveSummarizer()
        }.get(choice, FrequencyBasedSummarizer())

        summary = summarizer.summarize(video.transcript, percent)

        # Save summarization result
        summary_result = SummarizationResult.objects.create(
            video=video,
            summarization_type=choice,
            percent=percent,
            summary_text=summary
        )

        return JsonResponse({"summary": summary_result.summary_text})


class GetSummaryView(DetailView):
    model = SummarizationResult
    pk_url_kwarg = 'summary_id'

    def get(self, request, *args, **kwargs):
        summary_id = self.kwargs.get(self.pk_url_kwarg)
        summary = get_object_or_404(SummarizationResult, id=summary_id)
        return JsonResponse({"summary": summary.summary_text})


class DeleteSummaryView(DeleteView):
    model = SummarizationResult
    pk_url_kwarg = 'summary_id'

    def delete(self, request, *args, **kwargs):
        summary_id = self.kwargs.get(self.pk_url_kwarg)
        summary = get_object_or_404(SummarizationResult, id=summary_id)
        summary.delete()
        return JsonResponse({"message": "Summary deleted successfully"})
