# from django.http import Http404
from django.shortcuts import render
# from .models import Postforcegraph
# from django.http import JsonResponse
# import json
# from datetime import datetime
# from collections import OrderedDict
# from pages import views as main_view


def timelinegraph(request):
    # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').last()
    # posts = Post.objects.filter(published_date__lte=timezone.now())
    return render(request, 'pages/timelinegraph.html')