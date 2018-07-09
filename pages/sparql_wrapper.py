import json
from datetime import datetime
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from base64 import b64encode
from pages import extractor_transformation as extractor_trans


def call_api(sparql, link_query):
    values = urlencode(
        {
            'query': 'PREFIX aitslt:<http://www.semanticweb.org/milkk/ontologies/2017/11/testData#>' + sparql})
    credentials = b64encode('admin:admin'.encode('ascii'))  # username:password
    headers = {
        'Authorization': 'Basic %s' % credentials.decode('ascii'),
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/sparql-results+json'
    }
    data = values.encode('ascii')
    request = Request(link_query, data=data, headers=headers)
    try:
        response_body = json.loads(urlopen(request).read().decode('utf8'))
        return extractor_trans.transform_api(response_body)
    except HTTPError as e:
        print(e.code)
        print(e.reason)
        print(request.__dict__)
        response_body = {
            "head": {
                "vars": [
                    "subject",
                    "predicate",
                    "object"
                ]
            },
            "results": {
                "bindings": [
                    {
                        "subject": {
                            "type": "literal",
                            "value": "Error"
                        },
                        "predicate": {
                            "type": "literal",
                            "value": e.code
                        },
                        "object": {
                            "type": "literal",
                            "value": e.reason
                        }
                    }
                ]
            }
        }
        return response_body


def nested_filter_query(prefixes_list, subject_domain, predicate, list_object):
    nested = '{ select distinct ?subject where { ?subject rdf:type ' + subject_domain \
             + ' . ?subject ?predicate ?object . ' \
             + 'filter(?object != owl:NamedIndividual)'
    print(prefixes_list)  # && ?predicate != rdf:type
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
                    list_object[idx] = '"{}"^^xsd:dateTime'.format(each)
                    # list_object[idx] = '"{}"^^xsd:dateTime'.format(datetime.strptime(each, "%d %b'%y %H:%M:%S").isoformat())
            elif p in ['http://www.w3.org/1999/02/22-rdf-syntax-ns']:
                for idx, each in enumerate(list_object):
                    #  list_object[idx] = '<' + prefixes_list[0] + '#' + each + '>'
                    list_object[idx] = '<' + each + '>'
                    prefix_predicate = '<' + p + '#' + predicate + '>'
            else:
                prefix_predicate = '<' + p + '#' + predicate + '>'
    else:
        prefix_predicate = '<' + prefixes_list[0] + '#' + predicate + '>'
        for idx, each in enumerate(list_object):
            # list_object[idx] = '<' + prefixes_list[0] + '#' + each + '>'
            list_object[idx] = '<' + each + '>'

    nested += 'filter(?predicate = ' + prefix_predicate
    text = make_filter_sparql(list_object, 'object')

    nested += text + ')}}'
    return nested


def make_filter_sparql(list_filter, object_var):
    text = ''
    # print(list_filter)
    for idx, each in enumerate(list_filter):
        if idx == 0:
            text += ' && (?' + object_var + ' = ' + each
        else:
            text += ' || ?' + object_var + ' = ' + each
    if text != '':
        text += ')'
    return text