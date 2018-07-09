from django.http import Http404
from django.shortcuts import render
from pages import extractor_transformation as extractor_trans
from pages import sparql_wrapper as spql_wrapper
from .models import Postforcegraph, Timelinegraph
from django.http import JsonResponse
import json


def timelinegraph(request, post_id):
    try:
        # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').last()
        # posts = Post.objects.filter(published_date__lte=timezone.now())

        # project_data = Postforcegraph.objects.get(pk=4)
        project_data = Timelinegraph.objects.get(pk=post_id)
        date_show = project_data.date_marked.property_path
        results = extractor_trans.transform_api(project_data.source)
        filtering = extractor_trans.faceted_search(project_data.source, project_data.domain_subject.domain_path)
        new_results = []
        new_results.append(nested_transformation(results, "All", date_show.split('#')[-1]))

        # ======== temporary key =========
        project_data.title = project_data.page_title
        project_data.subject = project_data.domain_subject
        # ======== temporary key =========

        project_data.result = new_results
        project_data.save()

        # ======== compare facet to display  =========
        compare_facets = project_data.faceted_search.select_related()
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

        return render(request, 'pages/timelinegraph.html', {'posts': project_data, 'new_results': new_results,
                                                            'filter_facets': filtering['filter_facets'],
                                                            'filter_prefix': filtering['filter_prefixes'],
                                                            'dateShow': date_show.split('#')[-1]})
    except Timelinegraph.DoesNotExist:
        raise Http404("Post does not exist")


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
            print(request.POST)
            # print(request.POST.get('subject_domain'))
            # print(request.POST.keys())
            for k in request.POST.keys():
                if k == 'csrfmiddlewaretoken':
                    pass
                elif k == 'subject_domain':
                    pass
                elif k == 'date_show':
                    pass
                elif k == 'link_query':
                    link_query = request.POST.get('link_query')
                elif k == 'prefixes_query':
                    prefix_json = json.loads(request.POST.getlist(k)[0].replace("\'", "\""))
                else:
                    if k in prefix_json:
                        facetdata.extend(request.POST.getlist(k))
                        print(facetdata)
                        # print(request.POST.getlist(k))
                        sparql += spql_wrapper.nested_filter_query(prefix_json.get(k), domain_prefix_subject, k, request.POST.getlist(k))
            sparql += '}order by ?subject'
            results = spql_wrapper.call_api(sparql, link_query)

            for (i, item) in enumerate(facetdata):
                facetdata[i] = item.split('#')[-1]

            new_facetdata = []
            for result in results:
                if result.get('object') in facetdata:
                    if result.get('o_label') is not None:
                        new_facetdata.append(result.get('o_label'))
                        # facetdata[facetdata.index(result.get('object'))] = result.get('o_label')
                    else:
                        new_facetdata.append(result.get('object'))

            new_results = [nested_transformation(results, "All", request.POST.get('date_show'))]
    return JsonResponse({'filter_name': extractor_trans.list_facet(new_facetdata), 'status': sparql, 'query': new_results})
    # , 'dateShow': request.POST.get('date_show')


class Dictlist(dict):
    def __setitem__(self, key, value):
        try:
            self[key]
        except KeyError:
            super(Dictlist, self).__setitem__(key, [])
        self[key].append(value)
