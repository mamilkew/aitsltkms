from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from .models import Post
from django.http import HttpResponse, JsonResponse
import os
import json


# Create your views here.


def index(request):
    posts = Post.objects.filter(published_date__lte=timezone.now())
    return render(request, 'pages/index.html', {'posts': posts})


def filter_detail(request):
    if request.method == 'POST':
        if request.is_ajax():
            radiodata = request.POST.get('PJyear')
            print(radiodata)
            SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
            json_url = os.path.join(SITE_ROOT, "static/data", "PJ_filter_PJyear.json")
            data = json.load(open(json_url))
            results = data['results']['bindings']
            new_results = []

            # transform to pattern for visualization standard
            for result in results:
                tmp = {}
                tmp['subject'] = check_type(result.get('subject').get('type'), result.get('subject').get('value'))
                tmp['predicate'] = check_type(result.get('predicate').get('type'), result.get('predicate').get('value'))
                tmp['object'] = check_type(result.get('object').get('type'), result.get('object').get('value'))
                new_results.append(tmp)
                # print(new_results)

    return JsonResponse({'status': 'OK', 'filter_name': radiodata, 'query': new_results})


def detail(request, post_id):
    # posts = get_object_or_404(Post, pk=post_id)

    # SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    # json_url = os.path.join(SITE_ROOT, "static/data", "PJ_filter_PJyear.json")
    # data = json.load(open(json_url))
    # results = data['results']['bindings']
    # new_results = []

    try:
        posts = Post.objects.get(pk=post_id)
        results = posts.source['results']['bindings']
        new_results = []
        tmp_PJyear = []
        tmp_PJstatus = []
        # tmp_isRelatedTo = []

        # transform to pattern for visualization standard
        for result in results:
            tmp = {}
            tmp['subject'] = check_type(result.get('subject').get('type'), result.get('subject').get('value'))
            tmp['predicate'] = check_type(result.get('predicate').get('type'), result.get('predicate').get('value'))
            tmp['object'] = check_type(result.get('object').get('type'), result.get('object').get('value'))
            new_results.append(tmp)
            # print(new_results)
            if tmp['predicate'] == 'PJyear':
                tmp_PJyear.append(tmp['object'])  # {'PJyear': [2013, 2014, 2015, 2016]}
            elif tmp['predicate'] == 'PJstatus':
                tmp_PJstatus.append(tmp['object'])
            # elif tmp['predicate'] == 'isRelatedTo':
            #     tmp_isRelatedTo.append(tmp['object'])

        posts.result = new_results
        posts.save()
        filter_facets = {'PJyear': list_facet(tmp_PJyear),
                         'PJstatus': list_facet(tmp_PJstatus)}  # ,'isRelatedTo': list_facet(tmp_isRelatedTo)

    except Post.DoesNotExist:
        raise Http404("Question does not exist")

    return render(request, 'pages/detail.html', {'posts': posts, 'filter_facets': filter_facets})


def check_type(type_result, value):
    if type_result == "uri":
        return value.split('#')[-1]
    elif type_result == "literal":
        return value
    else:
        return ''


def list_facet(tmp_facets):
    facets = sorted(list(set(tmp_facets)))
    return facets
