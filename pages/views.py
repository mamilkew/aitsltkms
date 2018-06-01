from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.http import HttpResponse


# Create your views here.


def index(request):
    posts = Post.objects.filter(published_date__lte=timezone.now())

    return render(request, 'pages/index.html', {'posts': posts})
