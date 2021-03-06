from datetime import datetime
from collections import OrderedDict


# transform to pattern for visualization standard with file .json
# def transform_data(filename):
# SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
# json_url = os.path.join(SITE_ROOT, "static/data", filename)
# data = json.load(open(json_url))
# results = json.loads(data)['results']['bindings']

def transform_api(data):
    results = data['results']['bindings']
    new_results = []

    for result in results:
        tmp = {}
        tmp['subject'] = check_type(result.get('subject').get('datatype'), result.get('subject').get('type'),
                                    result.get('subject').get('value'))
        tmp['predicate'] = check_type(result.get('predicate').get('datatype'), result.get('predicate').get('type'),
                                      result.get('predicate').get('value'))
        tmp['object'] = check_type(result.get('object').get('datatype'), result.get('object').get('type'),
                                   result.get('object').get('value'))
        if result.get('s_label') is not None:
            tmp['s_label'] = result.get('s_label').get('value')
        if result.get('p_label') is not None:
            tmp['p_label'] = result.get('p_label').get('value')
        if result.get('o_label') is not None:
            tmp['o_label'] = result.get('o_label').get('value')
        new_results.append(tmp)
    return new_results


def check_type(datatype_result, type_result, value):
    if type_result == "uri":
        return value.split('#')[-1]
    elif type_result == "literal":
        if (datatype_result == "http://www.w3.org/2001/XMLSchema#dateTime"):
            date_format = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S').date()
            return date_format.strftime("%d %b'%y %H:%M:%S")
        elif (datatype_result == "http://www.w3.org/2001/XMLSchema#float"):
            return value
        else:
            return value
    else:
        return ''


def list_facet(tmp_facets):
    facets = sorted(list(set(tmp_facets)))
    return facets


def faceted_search(data, subject_domain):
    results = data['results']['bindings']
    filter_facets = {}
    filter_prefixes = {}

    for result in results:
        tmp = {}
        # tmp['subject'] = check_type(result.get('subject').get('datatype'), result.get('subject').get('type'),
        #                             result.get('subject').get('value'))
        tmp['predicate'] = check_type(result.get('predicate').get('datatype'), result.get('predicate').get('type'),
                                      result.get('predicate').get('value'))
        tmp['object'] = check_type(result.get('object').get('datatype'), result.get('object').get('type'),
                                   result.get('object').get('value'))
        # if result.get('s_label') is not None:
        #     tmp['s_label'] = result.get('s_label').get('value')
        if result.get('p_label') is not None:
            tmp['p_label'] = result.get('p_label').get('value')
        if result.get('o_label') is not None:
            # tmp['o_label'] = result.get('o_label').get('value')
            tmp['object'] = result.get('o_label').get('value')

        #  ===== making a list of Filtering >> add to filter_prefixes to make Facet =====
        if tmp['predicate'] in filter_facets:
            tmp_filter = filter_facets.get(tmp['predicate'])[0]
            tmp_filter[result.get('object').get('value')] = tmp['object']
            filter_facets[tmp['predicate']][0] = dict(sorted(tmp_filter.items()))
            # filter_facets[tmp['predicate']][0] = list_facet(tmp_filter)
        else:
            if tmp.get('p_label') is not None:
                filter_facets[tmp['predicate']] = [{result.get('object').get('value'): tmp['object']}, tmp['p_label']]
            else:
                filter_facets[tmp['predicate']] = [{result.get('object').get('value'): tmp['object']}, tmp['predicate']]

        # if tmp['predicate'] in filter_facets:
        #     tmp_filter = filter_facets.get(tmp['predicate'])[0]
        #     tmp_filter.append(tmp['object'])
        #     filter_facets[tmp['predicate']][0] = list_facet(tmp_filter)
        # else:
        #     if tmp.get('p_label') is not None:
        #         filter_facets[tmp['predicate']] = [[tmp['object']], tmp['p_label']]
        #     else:
        #         filter_facets[tmp['predicate']] = [[tmp['object']], tmp['predicate']]

        #  ===== making a list of prefixes =====
        # prefix_subject = check_prefix(result.get('subject').get('datatype'), result.get('subject').get('type'),
        #                               result.get('subject').get('value'))
        # filter_prefixes = make_filter_prefixes(prefix_subject, subject_domain, filter_prefixes)
        #
        prefix_predicate = check_prefix(result.get('predicate').get('datatype'), result.get('predicate').get('type'),
                                        result.get('predicate').get('value'))
        filter_prefixes = make_filter_prefixes(prefix_predicate, tmp['predicate'], filter_prefixes)

        prefix_object = check_prefix(result.get('object').get('datatype'), result.get('object').get('type'),
                                     result.get('object').get('value'))
        filter_prefixes = make_filter_prefixes(prefix_object, tmp['predicate'], filter_prefixes)

    print(filter_facets)
    filter_facets = OrderedDict(sorted(filter_facets.items(), key=lambda t: t[0]))
    # print(dict(sorted(filter_facets.items())))

    return {'filter_facets': filter_facets, 'filter_prefixes': filter_prefixes}


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
        prefixes_dict[value] = list_facet(tmp_prefix)
        return prefixes_dict
    else:
        prefixes_dict[value] = [prefixes]
        return prefixes_dict


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


class Dictlist(dict):
    def __setitem__(self, key, value):
        try:
            self[key]
        except KeyError:
            super(Dictlist, self).__setitem__(key, [])
        self[key].append(value)
