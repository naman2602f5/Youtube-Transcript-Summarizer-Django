from django.db import models

class YouTubeVideo(models.Model):
    video_id = models.CharField(max_length=50, unique=True)
    youtube_url = models.URLField()
    transcript = models.TextField()
    language = models.CharField(max_length=50)

    class Meta:
        db_table = 'YouTubeVideo'

    def __str__(self):
        return self.video_id

class SummarizationResult(models.Model):
    video = models.ForeignKey(YouTubeVideo, on_delete=models.CASCADE)
    summarization_type = models.CharField(max_length=50)
    percent = models.FloatField()
    summary_text = models.TextField()

    class Meta:
        db_table = 'SummarizationResult'

    def __str__(self):
        return f"{self.summarization_type} summary of {self.video.video_id}"

class TranslationRecord(models.Model):
    video = models.ForeignKey(YouTubeVideo, on_delete=models.CASCADE)
    source_language = models.CharField(max_length=50)
    target_language = models.CharField(max_length=50, default="english")
    translated_text = models.TextField()

    class Meta:
        db_table = 'TranslationRecord'

    def __str__(self):
        return f"Translation of {self.video.video_id} from {self.source_language} to {self.target_language}"
