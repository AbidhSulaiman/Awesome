
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from a_posts.views import home_view, post_create_view, post_delete_view, post_edit_view, post_page_view, like_reply
from a_posts.views import like_post,comment_sent, comment_delete_view, reply_sent, reply_delete_view, like_comment
from a_users.views import profile_view, profile_edit_view, profile_delete_view
from a_inbox.views import inbox_view

urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('theboss/', admin.site.urls),
    
    path('accounts/', include('allauth.urls')),
    path('', home_view, name='home'),
    path('post/create/', post_create_view, name='post-create'),
    path('post/delete/<pk>/', post_delete_view, name='post-delete'),
    path('post/edit/<pk>/', post_edit_view, name='post-edit'),
    path('post/<pk>/', post_page_view, name='post'),
    path('post/<pk>/like/', like_post, name='like-post'),
    path('comment/like/<pk>/', like_comment, name='like-comment'),
    path('reply/like/<pk>/', like_reply, name='like-reply'),
    path('category/<taglabel>/', home_view, name='category'),
    path('profile/', profile_view, name='profile'),
    path('inbox/', include('a_inbox.urls')),
    path('<username>/', profile_view, name='userprofile'),
    path('profile/edit/', profile_edit_view, name='profile-edit'),
    path('profile/delete/', profile_delete_view, name='profile-delete'),
    path('profile/onboarding/', profile_edit_view, name='profile-onboarding'),
    path('commentsend/<pk>/', comment_sent, name = 'comment-sent'),
    path('comments/delete/<pk>/', comment_delete_view, name='comment-delete'),
    path('reply-send/<pk>/', reply_sent, name = 'reply-sent'),
    path('reply/delete/<pk>/', reply_delete_view, name='reply-delete'),
    
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)