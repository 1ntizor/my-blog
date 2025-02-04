from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from .forms import CommentForm
from django.db import models
from django.db.models import Q 


def post_list(request):
    category = request.GET.get('category', '')
    query = request.GET.get('q', '')
    posts = Post.objects.all().order_by('-created_at')

    if query:
        posts = posts.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    
    
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  

    
    return render(request, 'blog/post_lists.html', {'page_obj': page_obj, 'category': category, 'query': query})


def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request,'blog/post_create.html', {'form':form}) 


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request,'blog/post_edit.html', {'form': form, 'post': post})


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form':form})
