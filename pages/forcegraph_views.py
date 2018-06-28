from django.http import Http404
from django.shortcuts import render
from .models import Postforcegraph
from django.http import JsonResponse
import json
from datetime import datetime
from pages import extractor_transformation as extractor_trans


def forcegraph(request, post_id):
    try:
        posts = Postforcegraph.objects.get(pk=post_id)
        results = posts.source['results']['bindings']  # ===== get DB (from API when created) =====
        new_results = []
        filter_facets = {}
        filter_prefixes = {}

        #  ===== transform to pattern for visualization standard for direct-forcegraph =====
        for result in results:
            tmp = {}
            tmp['subject'] = extractor_trans.check_type(result.get('subject').get('datatype'), result.get('subject').get('type'),
                                        result.get('subject').get('value'))
            tmp['predicate'] = extractor_trans.check_type(result.get('predicate').get('datatype'), result.get('predicate').get('type'),
                                          result.get('predicate').get('value'))
            tmp['object'] = extractor_trans.check_type(result.get('object').get('datatype'), result.get('object').get('type'),
                                       result.get('object').get('value'))
            if result.get('s_label') is not None:
                tmp['s_label'] = result.get('s_label').get('value')
            if result.get('p_label') is not None:
                tmp['p_label'] = result.get('p_label').get('value')
            if result.get('o_label') is not None:
                tmp['o_label'] = result.get('o_label').get('value')
            new_results.append(tmp)

        filtering = extractor_trans.faceted_search(posts.source, posts.subject)
        posts.result = new_results
        # posts.result = transform_api(posts.source)
        posts.save()

        return render(request, 'pages/forcegraph.html',
                      {'posts': posts, 'filter_facets': filtering['filter_facets'], 'filter_prefix': filtering['filter_prefixes'],})

    except Postforcegraph.DoesNotExist:
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
                     + 'filter(?object != owl:NamedIndividual && ?predicate != rdf:type)'
            facetdata = ''
            # print(request.POST)
            # print(request.POST.get('subject_domain'))
            # print(request.POST.keys())
            for k in request.POST.keys():
                if k == 'csrfmiddlewaretoken':
                    pass
                elif k == 'subject_domain':
                    pass
                elif k == 'prefixes_query':
                    prefix_json = json.loads(request.POST.getlist(k)[0].replace("\'", "\""))
                else:
                    if k in prefix_json:
                        print(request.POST.getlist(k))
                        sparql += nested_filter_query(prefix_json.get(k), domain_prefix_subject, k, request.POST.getlist(k))
            sparql += '}order by ?subject'
            new_results = extractor_trans.call_api(sparql)

    return JsonResponse({'filter_name': facetdata, 'status': sparql, 'query': new_results})


def nested_filter_query(prefixes_list, subject_domain, predicate, list_object):
    nested = '{ select distinct ?subject where { ?subject rdf:type ' + subject_domain \
             + ' . ?subject ?predicate ?object . ' \
             + 'filter(?object != owl:NamedIndividual && ?predicate != rdf:type)'
    print(prefixes_list)
    if len(prefixes_list) == 2:
        for p in prefixes_list:
            if p in ['integer']:
                for idx, each in enumerate(list_object):
                    list_object[idx] = each
            elif p in ['float']:
                for idx, each in enumerate(list_object):
                    list_object[idx] = '"{}"^^xsd:float'.format(each)
            elif p in ['literal']:
                for idx, each in enumerate(list_object):
                    list_object[idx] = '"{}"'.format(each)
            elif p in ['dateTime']:
                for idx, each in enumerate(list_object):
                    list_object[idx] = '"{}"^^xsd:dateTime'.format(datetime.strptime(each, "%d %b'%y %H:%M:%S").isoformat())
            else:
                prefix_predicate = '<' + p + '#' + predicate + '>'
    else:
        prefix_predicate = '<' + prefixes_list[0] + '#' + predicate + '>'
        for idx, each in enumerate(list_object):
            list_object[idx] = '<' + prefixes_list[0] + '#' + each + '>'

    nested += 'filter(?predicate = ' + prefix_predicate
    text = extractor_trans.make_filter_sparql(list_object, 'object')

    nested += text + ')}}'
    return nested
