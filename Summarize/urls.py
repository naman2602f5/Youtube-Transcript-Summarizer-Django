from django.urls import path
from Summarize.views import FetchAndStoreVideoView, SummarizeTextView, GetSummaryView, DeleteSummaryView

urlpatterns = [
    path('fetch-video/', FetchAndStoreVideoView.as_view(), name='fetch_video'),
    path('api/summarize/', SummarizeTextView.as_view(), name='summarize_text'),
    path('get-summary/<int:summary_id>/', GetSummaryView.as_view(), name='get_summary'),
    path('delete-summary/<int:summary_id>/', DeleteSummaryView.as_view(), name='delete_summary'),
]