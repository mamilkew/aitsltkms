from django.http import Http404
from django.shortcuts import render
from .models import Forcegraph
from django.http import JsonResponse
import json
from pages import extractor_transformation as extractor_trans
from pages import sparql_wrapper as spql_wrapper


def forcegraph(request, post_id):
    try:
        posts = Forcegraph.objects.get(pk=post_id)  # ===== get DB (from API when created) =====

        #  ===== transform to pattern for visualization standard for s-p-o =====
        new_results = extractor_trans.transform_api(posts.source)

        #  ===== making a list of Filtering
        filtering = extractor_trans.faceted_search(posts.source, posts.domain_subject.domain_path)

        # ======== temporary key =========
        posts.title = posts.page_title
        posts.subject = posts.domain_subject
        # ======== temporary key =========

        posts.result = new_results
        posts.save()

        # ======== compare facet to display  =========
        compare_facets = posts.faceted_search.select_related()
        if compare_facets:
            tmps = {}
            for compare_facet in compare_facets:
                value = compare_facet.property_path.split('#')[1]
                if value in filtering['filter_facets']:
                    tmps[value] = filtering['filter_facets'][value]

            if 'type' in filtering['filter_facets']:
                tmps['type'] = filtering['filter_facets']['type']
            if 'comment' in filtering['filter_facets']:
                tmps['comment'] = filtering['filter_facets']['comment']
            if 'label' in filtering['filter_facets']:
                tmps['label'] = filtering['filter_facets']['label']

            filtering['filter_facets'] = tmps

        return render(request, 'pages/forcegraph.html',
                      {'posts': posts, 'filter_facets': filtering['filter_facets'],
                       'filter_prefix': filtering['filter_prefixes'], })

    except Forcegraph.DoesNotExist:
        raise Http404("Post does not exist")


#  Ajax from filter to call API then get result and display in existing page
def filter_query(request):
    if request.method == 'POST':
        if request.is_ajax():
            # prefix_data = request.POST.getlist('prefixes_query')[0]
            # domain_prefix = json.loads(prefix_data.replace("\'", "\"")).get(request.POST.get('subject_domain'))[0]
            # domain_prefix_subject = '<' + domain_prefix + '#' + request.POST.get('subject_domain') + '>'
            domain_prefix_subject = '<' + request.POST.get('subject_domain') + '>'
            sparql = 'SELECT DISTINCT * WHERE{?subject rdf:type ' + domain_prefix_subject + ' .' \
                     + '?subject ?predicate ?object . ' \
                     + 'optional{?subject rdfs:label ?s_label}' \
                     + 'optional{?predicate rdfs:label ?p_label}' \
                     + 'optional{?object rdfs:label ?o_label}' \
                     + 'filter(?object != owl:NamedIndividual)'  # && ?predicate != rdf:type
            facetdata = ''
            # print(request.POST)
            # print(request.POST.get('subject_domain'))
            # print(request.POST.keys())
            for k in request.POST.keys():
                if k == 'csrfmiddlewaretoken':
                    pass
                elif k == 'subject_domain':
                    pass
                elif k == 'link_query':
                    link_query = request.POST.get('link_query')
                elif k == 'prefixes_query':
                    prefix_json = json.loads(request.POST.getlist(k)[0].replace("\'", "\""))
                else:
                    if k in prefix_json:
                        print(request.POST.getlist(k))
                        sparql += spql_wrapper.nested_filter_query(prefix_json.get(k), domain_prefix_subject, k,
                                                                   request.POST.getlist(k))
            sparql += '}order by ?subject'
            new_results = spql_wrapper.call_api(sparql, link_query)

    return JsonResponse({'filter_name': facetdata, 'status': sparql, 'query': new_results})
