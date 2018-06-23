from django.http import Http404
from django.shortcuts import render
from .models import Postforcegraph
from django.http import JsonResponse
import json
from datetime import datetime
from collections import OrderedDict
from pages import views as main_view


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
            tmp['subject'] = main_view.check_type(result.get('subject').get('datatype'), result.get('subject').get('type'),
                                        result.get('subject').get('value'))
            tmp['predicate'] = main_view.check_type(result.get('predicate').get('datatype'), result.get('predicate').get('type'),
                                          result.get('predicate').get('value'))
            tmp['object'] = main_view.check_type(result.get('object').get('datatype'), result.get('object').get('type'),
                                       result.get('object').get('value'))
            if result.get('s_label'):
                tmp['s_label'] = result.get('s_label').get('value')
            if result.get('p_label'):
                tmp['p_label'] = result.get('p_label').get('value')
            if result.get('o_label'):
                tmp['o_label'] = result.get('o_label').get('value')
            new_results.append(tmp)

            #  ===== making a list of Filtering >> add to filter_prefixes to make Facet =====
            if tmp['predicate'] in filter_facets:
                tmp_filter = filter_facets.get(tmp['predicate'])[0]
                tmp_filter.append(tmp['object'])
                filter_facets[tmp['predicate']][0] = main_view.list_facet(tmp_filter)
            else:
                if tmp.get('p_label') is not None:
                    filter_facets[tmp['predicate']] = [[tmp['object']], tmp['p_label']]
                else:
                    filter_facets[tmp['predicate']] = [[tmp['object']], tmp['predicate']]

            #  ===== making a list of prefixes =====
            prefix_subject = check_prefix(result.get('subject').get('datatype'),
                                          result.get('subject').get('type'), result.get('subject').get('value'))
            filter_prefixes = make_filter_prefixes(prefix_subject, posts.subject, filter_prefixes)

            prefix_predicate = check_prefix(result.get('predicate').get('datatype'),
                                            result.get('predicate').get('type'), result.get('predicate').get('value'))
            filter_prefixes = make_filter_prefixes(prefix_predicate, tmp['predicate'], filter_prefixes)

            prefix_object = check_prefix(result.get('object').get('datatype'), result.get('object').get('type'),
                                         result.get('object').get('value'))
            filter_prefixes = make_filter_prefixes(prefix_object, tmp['predicate'], filter_prefixes)
        print(filter_facets)
        filter_facets = OrderedDict(sorted(filter_facets.items(), key=lambda t: t[0]))
        # print(dict(sorted(filter_facets.items())))

        posts.result = new_results
        # posts.result = transform_api(posts.source)
        posts.save()

        return render(request, 'pages/forcegraph.html',
                      {'posts': posts, 'filter_facets': filter_facets, 'filter_prefix': filter_prefixes})

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
            new_results = main_view.call_api(sparql)

    return JsonResponse({'filter_name': facetdata, 'status': sparql, 'query': new_results})


def nested_filter_query(prefixes_list, subject_domain, predicate, list_object):
    nested = '{ select distinct ?subject where { ?subject rdf:type ' + subject_domain \
             + ' . ?subject ?predicate ?object . ' \
             + 'filter(?object != owl:NamedIndividual && ?predicate != rdf:type)'
    print(prefixes_list)
    if len(prefixes_list) == 2:
        for p in prefixes_list:
            if p in ['integer', 'float']:
                for idx, each in enumerate(list_object):
                    list_object[idx] = each
            elif p in ['literal']:
                for idx, each in enumerate(list_object):
                    list_object[idx] = '"{}"'.format(each)
            elif p in ['dateTime']:
                for idx, each in enumerate(list_object):
                    list_object[idx] = '"{}"^^xsd:date'.format(datetime.strptime(each, "%d %b'%y").isoformat())
            else:
                prefix_predicate = '<' + p + '#' + predicate + '>'
    else:
        prefix_predicate = '<' + prefixes_list[0] + '#' + predicate + '>'
        for idx, each in enumerate(list_object):
            list_object[idx] = '<' + prefixes_list[0] + '#' + each + '>'

    nested += 'filter(?predicate = ' + prefix_predicate
    text = main_view.make_filter_sparql(list_object, 'object')

    nested += text + ')}}'
    return nested


def check_prefix(datatype_result, type_result, value):
    if type_result == "uri":
        return value.split('#')[0]
    elif type_result == "literal":
        if datatype_result is not None:
            return datatype_result.split('#')[1]
        else:
            return type_result
    else:
        return value


def make_filter_prefixes(prefixes, value, prefixes_dict):
    if value in prefixes_dict:
        tmp_prefix = prefixes_dict.get(value)
        tmp_prefix.append(prefixes)
        prefixes_dict[value] = main_view.list_facet(tmp_prefix)
        return prefixes_dict
    else:
        prefixes_dict[value] = [prefixes]
        return prefixes_dict