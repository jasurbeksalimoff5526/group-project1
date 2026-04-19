from django.urls import path
from .views import (
    PostListView, 
    PostDetailView, 
    PostCreateView, 
    AddReactionView, 
    PollVoteView
)

urlpatterns = [
    # Bosh sahifa - barcha postlar ro'yxati
    path('', PostListView.as_view(), name='post_list'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/reaction/', AddReactionView.as_view(), name='add_reaction'),
    path('poll/vote/<int:pk>/', PollVoteView.as_view(), name='poll_vote'),
]