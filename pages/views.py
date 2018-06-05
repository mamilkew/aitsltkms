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


def make_filter_script(list_filter):
    text = ''
    print(list_filter)
    for idx, each in enumerate(list_filter):
        if each.isdigit() == True:
            each = each
        else:
            each = '"{}"'.format(each)

        if idx == 0:
            text += ' && (?object = ' + each
        else:
            text += ' || ?object = ' + each
    if text != '':
        text += ')'
    return text


def filter_detail(request):
    if request.method == 'POST':
        if request.is_ajax():
            sparql = 'SELECT DISTINCT * WHERE{?subject rdf:type aitslt:Project .' \
                     + '?subject ?predicate ?object . filter(?object != owl:NamedIndividual && ?predicate != rdf:type)' \
                     + '{ select distinct ?subject where { ?subject rdf:type aitslt:Project . ?subject ?predicate ?object . ' \
                     + 'filter(?object != owl:NamedIndividual && ?predicate != rdf:type)'
            facetdata = ''

            if request.POST.get('PJyear') is not None:
                facetdata += 'PJyear'
                print(request.POST)
                pjyeardata = request.POST.getlist('PJyear')
                text = make_filter_script(pjyeardata)

                if request.POST.get('PJstatus') is not None:
                    sparql += 'filter(?predicate = aitslt:PJyear' + text + ')}'
                    facetdata += 'PJstatus'
                    pjstatusdata = request.POST.getlist('PJstatus')
                    filter_text = make_filter_script(pjstatusdata)
                    sparql_add = '}{ select distinct ?subject where { ?subject rdf:type aitslt:Project . ?subject ?predicate ?object . ' \
                                 + 'filter(?object != owl:NamedIndividual && ?predicate != rdf:type) '
                    sparql += sparql_add + 'filter(?predicate = aitslt:PJstatus' + filter_text + ')' + '}}}order by ?subject'
                else:
                    sparql += 'filter(?predicate = aitslt:PJyear' + text + ')' + '}}}order by ?subject'

                new_results = transform_data("PJ_filter_PJyear.json")

            elif request.POST.get('PJstatus') is not None:
                facetdata += 'PJstatus'
                pjstatusdata = request.POST.getlist('PJstatus')
                text = make_filter_script(pjstatusdata)
                sparql += 'filter(?predicate = aitslt:PJstatus' + text + ')' + '}}}order by ?subject'
                new_results = transform_data("PJ_filter_PJstatus.json")

            else:
                sparql += '}}}order by ?subject'

                new_results = transform_data("select_project.json")
                return JsonResponse({'filter_name': 'No Filter', 'status': sparql, 'query': new_results})

    return JsonResponse({'filter_name': facetdata, 'status': sparql, 'query': new_results})


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


# transform to pattern for visualization standard
def transform_data(filename):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data", filename)
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
    return new_results
