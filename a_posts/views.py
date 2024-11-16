from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Post, Tag, Comment, Reply
from .forms import PostCreateForm, PostEditForm, CommentCreateForm, ReplyCreateForm
from bs4 import BeautifulSoup
import requests
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import like_toggle
from django.core.paginator import Paginator



def home_view(request, taglabel= None):
    
    if taglabel:
        posts = Post.objects.filter(tag__slug = taglabel)
        taglabel = get_object_or_404(Tag, slug = taglabel)
    else:
        posts = Post.objects.all()
    
    paginator = Paginator(posts, 3)
    page = int(request.GET.get('page',1))
    
    try:
        posts = paginator.page(page)
    except:
        return HttpResponse('')
        
    context = {
        'posts':posts,
        'tag':taglabel,
        'page':page
    }
    
    if request.htmx:
        return render(request, 'snippets/loop_home_posts.html', context)
    
    return render(request, 'a_posts/home.html', context)

    
@login_required   
def post_create_view(request):
    
    if request.method == 'POST':
        form = PostCreateForm(data = request.POST)
        
        if form.is_valid():
            
            post = form.save(commit=False)
            website = requests.get(form.data['url'])
            source_code = BeautifulSoup(website.text, 'html.parser')
            
            find_image = source_code.select('meta[content^="https://live.staticflickr.com/"]')
            image = find_image[0]['content']
            post.image = image
            
            find_title = source_code.select('h1.photo-title')
            title = find_title[0].text.strip()
            post.title = title
            
            find_artist = source_code.select('a.owner-name')
            artist = find_artist[0].text.strip()
            post.artist = artist
            
            post.author = request.user

            post.save()
            form.save_m2m()
            
            return redirect('home')
        else:
            return HttpResponse('Post is unsuccefull')
            
    
    else:
        form = PostCreateForm()
    context = {'form':form}
    return render(request, 'a_posts/post_create.html', context)


@login_required
def post_delete_view(request, pk):
    
    if request.method =='POST':
        post = get_object_or_404(Post, id=pk, author = request.user)
        post.delete()
        messages.success(request, 'Post deleted')
        
        return redirect('home')
    else:
        post = get_object_or_404(Post, id=pk)
    
    context = {'post':post}
    return render(request, 'a_posts/post_delete.html', context)

@login_required
def post_edit_view(request, pk):
    post = get_object_or_404(Post, id=pk, author = request.user)
    form = PostEditForm(instance=post)
    if request.method == 'POST':
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post Updated')
            return redirect('home')

    context = {'post':post, 'form':form}
    return render(request, 'a_posts/post_edit.html', context)


def post_page_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    
    comment_form = CommentCreateForm()
    reply_form = ReplyCreateForm()
    
    if request.htmx:
        if 'top' in request.GET:
            # comments = post.comments.filter(likes__isnull=False).distinct()
            comments = post.comments.annotate(num_likes = Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
        else:
            comments = post.comments.all()
        return render(request, 'snippets/loop_postpage_comments.html', {'comments':comments,'reply_form':reply_form})
    
    context = {
        'post':post,
        'comment_form':comment_form,
        'reply_form':reply_form,
    }
    return render(request, 'a_posts/post_page.html', context)


@login_required
def comment_sent(request, pk):
    post = get_object_or_404(Post, id=pk)
    replayform = ReplyCreateForm()
    
    if request.method == 'POST':
        form = CommentCreateForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent_post = post
            comment.save()
    
    context = {
        'comment':comment,
        'post':post,
        'reply_form':replayform
    }
        
    return render(request, 'snippets/add_comment.html', context)


@login_required
def comment_delete_view(request, pk):
    
    post = get_object_or_404(Comment, id=pk, author = request.user)
    
    if request.method =='POST':
        post.delete()
        messages.success(request, 'Comment deleted')
        
        return redirect('post', post.parent_post.id)

    
    context = {'comment':post}
    return render(request, 'a_posts/comment_delete.html', context)

@login_required
def reply_sent(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    replayform = ReplyCreateForm()
    
    if request.method == 'POST':
        form = ReplyCreateForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parent_Comment = comment
            reply.save()
            
    context = {
        'comment':comment,
        'reply':reply,
        'reply_form':replayform,
    }
    return render(request, 'snippets/add_reply.html', context)

@login_required
def reply_delete_view(request, pk):
    
    reply = get_object_or_404(Reply, id=pk, author = request.user)
    
    if request.method =='POST':
        reply.delete()
        messages.success(request, 'Reply deleted')
        
        return redirect('post', reply.parent_Comment.parent_post.id)

    
    context = {'reply':reply}
    return render(request, 'a_posts/reply_delete.html', context)


@login_required
@like_toggle(Post)
def like_post(request, post):
          
    context = {
        'post':post
    }
    return render(request, 'snippets/likes.html', context)


@login_required
@like_toggle(Comment)
def like_comment(request, post):
          
    context = {
        'comment':post
    }
    return render(request, 'snippets/likes_comment.html', context)


@login_required
@like_toggle(Reply)
def like_reply(request, post):
          
    context = {
        'reply':post
    }
    return render(request, 'snippets/likes_reply.html', context)