from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello_world, name='index'),
    path('api/summarize', views.get_summarized_text, name='get_summarized_text'),
]