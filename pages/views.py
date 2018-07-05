from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from .models import Post, Forcegraph
from django.http import HttpResponse, JsonResponse
from pages import extractor_transformation as extractor_trans
from pages import sparql_wrapper as spql_wrapper
import os


def index(request):
    # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').last()
    posts = Forcegraph.objects.filter(published_date__lte=timezone.now())
    return render(request, 'pages/index.html', {'posts': posts})


def detail(request, post_id):
    # posts = get_object_or_404(Post, pk=post_id)

    # SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    # json_url = os.path.join(SITE_ROOT, "static/data", "PJ_filter_PJyear.json")
    # data = json.load(open(json_url))
    # results = data['results']['bindings']
    # new_results = []

    try:
        posts = Post.objects.get(pk=post_id)
        results = posts.source['results']['bindings']  # get DB (from API)
        new_results = []
        tmp_PJyear = []
        tmp_PJstatus = []
        tmp_isRelatedTo = []

        # transform to pattern for visualization standard
        for result in results:
            tmp = {}
            tmp['subject'] = extractor_trans.check_type(result.get('subject').get('datatype'),
                                                        result.get('subject').get('type'),
                                                        result.get('subject').get('value'))
            tmp['predicate'] = extractor_trans.check_type(result.get('predicate').get('datatype'),
                                                          result.get('predicate').get('type'),
                                                          result.get('predicate').get('value'))
            tmp['object'] = extractor_trans.check_type(result.get('object').get('datatype'),
                                                       result.get('object').get('type'),
                                                       result.get('object').get('value'))
            new_results.append(tmp)

            #  make the list of ----facets---- and value
            if tmp['predicate'] == 'PJyear':
                tmp_PJyear.append(tmp['object'])  # {'PJyear': [2013, 2014, 2015, 2016]}
            elif tmp['predicate'] == 'PJstatus':
                tmp_PJstatus.append(tmp['object'])
            elif tmp['predicate'] == 'isRelatedTo':
                tmp_isRelatedTo.append(tmp['object'])

        posts.result = new_results
        posts.save()

        # get DB (from API) ----facet_donor----
        tmp_isSponsoredBy = advance_facet(posts.facet_donor['head']['vars'][0],
                                          posts.facet_donor['results']['bindings'])
        # ----facet_country----
        tmp_isImplementedIn = advance_facet(posts.facet_country['head']['vars'][0],
                                            posts.facet_country['results']['bindings'])
        # ----facet_organizationunit----
        tmp_isImplementedBy = advance_facet(posts.facet_organizationunit['head']['vars'][0],
                                            posts.facet_organizationunit['results']['bindings'])
        # ----facet_person----
        tmp_person = advance_facet(posts.facet_person['head']['vars'][0], posts.facet_person['results']['bindings'])

        filter_facets = {'PJyear': extractor_trans.list_facet(tmp_PJyear),
                         'PJstatus': extractor_trans.list_facet(tmp_PJstatus),
                         'isSponsoredBy': extractor_trans.list_facet(tmp_isSponsoredBy),
                         'isImplementedIn': extractor_trans.list_facet(tmp_isImplementedIn),
                         'isImplementedBy': extractor_trans.list_facet(tmp_isImplementedBy),
                         'includesPerson': extractor_trans.list_facet(tmp_person),
                         'isRelatedTo': extractor_trans.list_facet(tmp_isRelatedTo)}

    except Post.DoesNotExist:
        raise Http404("Question does not exist")

    return render(request, 'pages/detail.html', {'posts': posts, 'filter_facets': filter_facets})


def advance_facet(facet_head, facet_result):
    tmp_list = []
    # print(facet_head)
    for each in facet_result:
        tmp_list.append(
            extractor_trans.check_type(each.get(facet_head).get('datatype'), each.get(facet_head).get('type'),
                                       each.get(facet_head).get('value')))
    return tmp_list


#  Ajax from filter in detail page for call API to get result and display in existing page
def filter_detail(request):
    if request.method == 'POST':
        if request.is_ajax():
            sparql = 'SELECT DISTINCT * WHERE{?subject rdf:type aitslt:Project .' \
                     + '?subject ?predicate ?object . filter(?object != owl:NamedIndividual && ?predicate != rdf:type)'
            facetdata = ''
            print(request.POST)

            if request.POST.get('PJyear') is not None:
                facetdata += 'PJyear'
                list_data = request.POST.getlist('PJyear')
                sparql += make_nested_filter('PJyear', list_data)
                # new_results = transform_data("PJ_filter_PJyear.json")

            if request.POST.get('PJstatus') is not None:
                facetdata += 'PJstatus'
                list_data = request.POST.getlist('PJstatus')
                sparql += make_nested_filter('PJstatus', list_data)
                # new_results = transform_data("PJ_filter_PJstatus.json")

            if request.POST.get('isRelatedTo') is not None:
                facetdata += 'isRelatedTo'
                list_data = request.POST.getlist('isRelatedTo')
                sparql += make_nested_filter('isRelatedTo', list_data)
                # new_results = transform_data("PJ_filter_isRelatedTo.json")

            if request.POST.get('isSponsoredBy') is not None:
                facetdata += 'isSponsoredBy'
                list_data = request.POST.getlist('isSponsoredBy')
                sparql += make_nested_filter('isSponsoredBy', list_data)

            if request.POST.get('isImplementedIn') is not None:
                facetdata += 'isImplementedIn'
                list_data = request.POST.getlist('isImplementedIn')
                sparql += make_nested_filter('isImplementedIn', list_data)

            if request.POST.get('isImplementedBy') is not None:
                facetdata += 'isImplementedBy'
                list_data = request.POST.getlist('isImplementedBy')
                sparql += make_nested_filter('isImplementedBy', list_data)

            if request.POST.get('includesPerson') is not None:
                facetdata += 'includesPerson'
                list_data = request.POST.getlist('includesPerson')
                sparql += make_nested_filter('includesPerson', list_data)

            sparql += '}order by ?subject'

            new_results = spql_wrapper.call_api(sparql, request.POST.get('link_query'))

            # new_results = transform_data("select_project.json")  # response_body

    return JsonResponse({'filter_name': facetdata, 'status': sparql, 'query': new_results})


def make_nested_filter(predicate, list_object):
    if predicate in ('isRelatedTo', 'isImplementedIn', 'isImplementedBy', 'isSponsoredBy', 'includesPerson'):
        for idx, each in enumerate(list_object):
            list_object[idx] = 'aitslt:{}'.format(each)
    if predicate == 'PJstatus':
        for idx, each in enumerate(list_object):
            list_object[idx] = '"{}"'.format(each)
    nested = '{ select distinct ?subject where { ?subject rdf:type aitslt:Project . ?subject ?predicate ?object . ' \
             + 'filter(?object != owl:NamedIndividual && ?predicate != rdf:type)'

    if predicate == 'isSponsoredBy':
        nested += 'optional{?object rdf:type ?donor .} filter(?predicate = aitslt:' + predicate
        text = spql_wrapper.make_filter_sparql(list_object, 'donor')
    elif predicate == 'isImplementedBy':
        nested += 'optional{?object aitslt:under ?organizationunit .} filter(?predicate = aitslt:' + predicate
        text = spql_wrapper.make_filter_sparql(list_object, 'organizationunit')
    elif predicate == 'includesPerson':
        nested += 'optional{?object rdf:type ?person .} filter((?predicate = aitslt:includesInvestigator ' \
                  + '|| ?predicate = aitslt:includesMember)'
        text = spql_wrapper.make_filter_sparql(list_object, 'person')
    else:
        nested += 'filter(?predicate = aitslt:' + predicate
        text = spql_wrapper.make_filter_sparql(list_object, 'object')

    nested += text + ')}}'
    return nested
