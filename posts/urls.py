from django.contrib import admin
from django.shortcuts import  render
from django.urls import path, include
from .views import CreatePost, CreateComment, CommentReply, delete_post, like_post, save_post, delete_comment, comment_like

urlpatterns = [
    # path('success/', lambda request: render(request, 'image_success.html'), name='image_success'),
    path('create/', CreatePost.as_view(), name='create_post'),
    path('<int:post_id>/delete/', delete_post, name='delete_post'),
    path('<int:post_id>/like_post', like_post, name='like_post'),
    path('<int:post_id>/save_post', save_post, name='save_post'),
    path('<int:post_id>/comment', CreateComment.as_view(), name='create_comment'),
    path('<int:comment_id>/delete_comment', delete_comment, name='delete_comment'),
    path('<int:comment_id>/comment_reply', CommentReply.as_view(), name='comment_reply'),
    path('<int:comment_id>/comment_like', comment_like, name='comment_like'),
    
]