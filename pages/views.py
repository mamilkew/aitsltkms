from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from .models import Post
from django.http import HttpResponse
import os
import json

# Create your views here.


def index(request):
    posts = Post.objects.filter(published_date__lte=timezone.now())
    return render(request, 'pages/index.html', {'posts': posts})


def detail(request, post_id):
    # posts = get_object_or_404(Post, pk=post_id)
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data", "PJ_filter_PJyear.json")
    data = json.load(open(json_url))
    results = data['results']['bindings']
    new_results = []

    for result in results:
        tmp = {}
        tmp['subject'] = check_type(result.get('subject').get('type'), result.get('subject').get('value'))
        tmp['predicate'] = check_type(result.get('predicate').get('type'), result.get('predicate').get('value'))
        tmp['object'] = check_type(result.get('object').get('type'), result.get('object').get('value'))
        new_results.append(tmp)
        # print(new_results)

    try:
        posts = Post.objects.get(pk=post_id)
        # transform to pattern for visualization standard
        posts.result = new_results
        posts.save()
        #

    except Post.DoesNotExist:
        raise Http404("Question does not exist")

    return render(request, 'pages/detail.html', {'posts': posts})


def check_type(type_result, value):
    if type_result == "uri":
        return value.split('#')[-1]
    elif type_result == "literal":
        return value
    else:
        return ''
