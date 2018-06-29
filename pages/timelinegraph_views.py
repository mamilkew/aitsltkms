# from django.http import Http404
from django.shortcuts import render
from pages import extractor_transformation as extractor_trans
from pages import sparql_wrapper as spql_wrapper
from .models import Postforcegraph
from django.http import JsonResponse
import json


def timelinegraph(request):
    # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').last()
    # posts = Post.objects.filter(published_date__lte=timezone.now())

    project_data = Postforcegraph.objects.get(pk=4)
    date_show = "PJend"
    results = extractor_trans.transform_api(project_data.source)
    filtering = extractor_trans.faceted_search(project_data.source, project_data.subject)
    new_results = []
    new_results.append(nested_transformation(results, "All", date_show))
    print(filtering)
    return render(request, 'pages/timelinegraph.html', {'posts': project_data, 'new_results': new_results,
                                                        'filter_facets': filtering['filter_facets'],
                                                        'filter_prefix': filtering['filter_prefixes'],
                                                        'dateShow': date_show})


def nested_transformation(results, group, date_show):
    new_result = {"name": group, "commits": []}
    for result in results:
        if result.get('s_label') is not None:
            s_label = result.get('s_label')
        else:
            s_label = result.get('subject')

        if result.get('p_label') is not None:
            p_label = result.get('p_label')
        else:
            p_label = result.get('predicate')

        if result.get('o_label') is not None:
            o_label = result.get('o_label')
        else:
            o_label = result.get('object')

        if date_show == result.get('predicate'):
            date_show = p_label

        check_index = next(
            (index for (index, d) in enumerate(new_result['commits']) if d["subject"] == [s_label]), None)
        if check_index is not None:  # result.get('subject') in new_results['commits'].values()
            tmp = new_result['commits'][check_index]
            tmp[p_label] = o_label
        else:
            tmp = Dictlist()
            tmp['subject'] = s_label
            tmp[p_label] = o_label
            new_result['commits'].append(tmp)
    new_result['date_show'] = date_show
    return new_result


def filter_timeline(request):
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
            facetdata = []
            # print(request.POST)
            # print(request.POST.get('subject_domain'))
            # print(request.POST.keys())
            for k in request.POST.keys():
                if k == 'csrfmiddlewaretoken':
                    pass
                elif k == 'subject_domain':
                    pass
                elif k == 'date_show':
                    pass
                elif k == 'prefixes_query':
                    prefix_json = json.loads(request.POST.getlist(k)[0].replace("\'", "\""))
                else:
                    if k in prefix_json:
                        facetdata.extend(request.POST.getlist(k))
                        print(facetdata)
                        sparql += spql_wrapper.nested_filter_query(prefix_json.get(k), domain_prefix_subject, k, request.POST.getlist(k))
            sparql += '}order by ?subject'
            results = spql_wrapper.call_api(sparql)

            for result in results:
                if result.get('o_label') is not None:
                    if result.get('object') in facetdata:
                        facetdata[facetdata.index(result.get('object'))] = result.get('o_label')

            new_results = [nested_transformation(results, "All", request.POST.get('date_show'))]
    return JsonResponse({'filter_name': facetdata, 'status': sparql, 'query': new_results})
    # , 'dateShow': request.POST.get('date_show')


class Dictlist(dict):
    def __setitem__(self, key, value):
        try:
            self[key]
        except KeyError:
            super(Dictlist, self).__setitem__(key, [])
        self[key].append(value)
