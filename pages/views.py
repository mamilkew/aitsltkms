# from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from .models import Post
from django.http import HttpResponse


# Create your views here.


def index(request):
    posts = Post.objects.filter(published_date__lte=timezone.now())
    return render(request, 'pages/index.html', {'posts': posts})


def detail(request, post_id):
    posts = get_object_or_404(Post, pk=post_id)
    # try:
    #     posts = Post.objects.get(pk=post_id)
    # except Post.DoesNotExist:
    #     raise Http404("Question does not exist")
    return render(request, 'pages/detail.html', {'posts': posts})
