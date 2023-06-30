from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import Post, Comment, Like
from .forms import PostForm, CommentForm

User = get_user_model()

def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if request.user.is_authenticated:
        if request.user != user_to_follow:
            request.user.following.add(user_to_follow)
    return redirect('feed')

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Assign the authenticated user
            post.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post)
    comment_form = CommentForm()
    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('feed')
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form, 'post': post})
def feed(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('feed')
    else:
        form = PostForm()

    posts = Post.objects.all().order_by('-created_at')
    comments = Comment.objects.filter(post__in=posts)

    likes = []
    if request.user.is_authenticated:
        liked_posts = Like.objects.filter(post__in=posts, user=request.user)
        likes = [liked_post.post_id for liked_post in liked_posts]

    if request.method == 'POST' and 'content' in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post_id = request.POST['post_id']
            comment.save()
            return redirect('feed')
    else:
        comment_form = CommentForm()

    return render(request, 'feed.html', {'posts': posts, 'comments': comments, 'likes': likes, 'form': form, 'comment_form': comment_form})

def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
    return redirect('feed')

