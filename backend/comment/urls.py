from django.urls import path

from comment.views import CommentsView

urlpatterns = [
    path('<int:post_id>/', CommentsView.as_view()),
    ]
