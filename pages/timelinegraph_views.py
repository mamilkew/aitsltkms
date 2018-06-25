# from django.http import Http404
from django.shortcuts import render
from pages import views as main_view


# from .models import Postforcegraph
# from django.http import JsonResponse
# import json
# from datetime import datetime
# from collections import OrderedDict
# from pages import views as main_view


def timelinegraph(request):
    # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').last()
    # posts = Post.objects.filter(published_date__lte=timezone.now())

    test_data = {
        "head": {
            "vars": [
                "subject",
                "predicate",
                "object",
                "s_label",
                "p_label",
                "o_label"
            ]
        },
        "results": {
            "bindings": [
                {
                    "subject": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#SET-2009-A004"
                    },
                    "predicate": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#PJkeyword"
                    },
                    "object": {
                        "type": "literal",
                        "value": "Dual Degree Masters"
                    },
                    "p_label": {
                        "type": "literal",
                        "value": "Project Keyword"
                    }
                },
                {
                    "subject": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#SET-2009-A004"
                    },
                    "predicate": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#PJkeyword"
                    },
                    "object": {
                        "type": "literal",
                        "value": "Transportation Engineering"
                    },
                    "p_label": {
                        "type": "literal",
                        "value": "Project Keyword"
                    }
                },
                {
                    "subject": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#SET-2009-A004"
                    },
                    "predicate": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#PJbaht"
                    },
                    "object": {
                        "datatype": "http://www.w3.org/2001/XMLSchema#float",
                        "type": "literal",
                        "value": "2920000.0"
                    }
                },
                {
                    "subject": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#SET-2009-A004"
                    },
                    "predicate": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#PJend"
                    },
                    "object": {
                        "datatype": "http://www.w3.org/2001/XMLSchema#dateTime",
                        "type": "literal",
                        "value": "2010-06-30T00:00:00"
                    }
                },
                {
                    "subject": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#SET-2009-A004"
                    },
                    "predicate": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#PJyear"
                    },
                    "object": {
                        "datatype": "http://www.w3.org/2001/XMLSchema#integer",
                        "type": "literal",
                        "value": "2009"
                    }
                },
                {
                    "subject": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#SET-2009-A004"
                    },
                    "predicate": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#TypeOfProject"
                    },
                    "object": {
                        "type": "literal",
                        "value": "Academic project"
                    }
                },
                {
                    "subject": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#SET-2009-A004"
                    },
                    "predicate": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#PJstart"
                    },
                    "object": {
                        "datatype": "http://www.w3.org/2001/XMLSchema#dateTime",
                        "type": "literal",
                        "value": "2009-02-01T00:00:00"
                    }
                },
                {
                    "subject": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#SET-2009-A004"
                    },
                    "predicate": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#PJstatus"
                    },
                    "object": {
                        "type": "literal",
                        "value": "Completed"
                    }
                },
                {
                    "subject": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#SET-2009-A004"
                    },
                    "predicate": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#isImplementedIn"
                    },
                    "object": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#AIT"
                    }
                },
                {
                    "subject": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#SET-2009-A004"
                    },
                    "predicate": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#isImplementedIn"
                    },
                    "object": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#Thailand"
                    }
                },
                {
                    "subject": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#SET-2009-A004"
                    },
                    "predicate": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#includesInvestigator"
                    },
                    "object": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#Kunnawee"
                    }
                },
                {
                    "subject": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#SET-2009-A004"
                    },
                    "predicate": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#isImplementedBy"
                    },
                    "object": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#te-fos"
                    }
                },
                {
                    "subject": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#SET-2009-A004"
                    },
                    "predicate": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#NameOfProject"
                    },
                    "object": {
                        "type": "literal",
                        "value": "Dual Degree Master Program in Transportation Engineering in Indonesia (Second Batch)"
                    }
                },
                {
                    "subject": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#SET-2009-A004"
                    },
                    "predicate": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#PJContractedAmount"
                    },
                    "object": {
                        "datatype": "http://www.w3.org/2001/XMLSchema#float",
                        "type": "literal",
                        "value": "2920000.0"
                    }
                },
                {
                    "subject": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#SET-2009-A004"
                    },
                    "predicate": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#isRelatedTo"
                    },
                    "object": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#TransportationEngineering-area"
                    }
                },
                {
                    "subject": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#SET-2009-A004"
                    },
                    "predicate": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#isSponsoredBy"
                    },
                    "object": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#ManderPortmanWoodward"
                    },
                    "o_label": {
                        "type": "literal",
                        "value": "MPW"
                    }
                },
                {
                    "subject": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#SET-2009-A007"
                    },
                    "predicate": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#isRelatedTo"
                    },
                    "object": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#AgriculturalWaterManagement-area"
                    }
                },
                {
                    "subject": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#SET-2009-A007"
                    },
                    "predicate": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#isSponsoredBy"
                    },
                    "object": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#DWF"
                    }
                },
                {
                    "subject": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#SET-2009-A007"
                    },
                    "predicate": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#isImplementedIn"
                    },
                    "object": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#Thailand"
                    }
                },
                {
                    "subject": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#SET-2009-A007"
                    },
                    "predicate": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#isSponsoredBy"
                    },
                    "object": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#FederationInternationalVehiculesAnciens"
                    }
                },
                {
                    "subject": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#SET-2009-A007"
                    },
                    "predicate": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#isSponsoredBy"
                    },
                    "object": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#FacultyOfLifeSciencesOfTheUniversityOfCopenhagen"
                    }
                },
                {
                    "subject": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#SET-2009-A007"
                    },
                    "predicate": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#PJyear"
                    },
                    "object": {
                        "datatype": "http://www.w3.org/2001/XMLSchema#integer",
                        "type": "literal",
                        "value": "2009"
                    }
                },
                {
                    "subject": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#SET-2009-A007"
                    },
                    "predicate": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#TypeOfProject"
                    },
                    "object": {
                        "type": "literal",
                        "value": "Workshop/Training"
                    }
                },
                {
                    "subject": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#SET-2009-A007"
                    },
                    "predicate": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#PJstatus"
                    },
                    "object": {
                        "type": "literal",
                        "value": "Completed"
                    }
                },
                {
                    "subject": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#SET-2009-A007"
                    },
                    "predicate": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#isImplementedBy"
                    },
                    "object": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#wem-fos"
                    }
                },
                {
                    "subject": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#SET-2009-A007"
                    },
                    "predicate": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#includesInvestigator"
                    },
                    "object": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#Mukand_Singh"
                    }
                },
                {
                    "subject": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#SET-2009-A007"
                    },
                    "predicate": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#PJend"
                    },
                    "object": {
                        "datatype": "http://www.w3.org/2001/XMLSchema#dateTime",
                        "type": "literal",
                        "value": "2010-08-31T00:00:00"
                    }
                },
                {
                    "subject": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#SET-2009-A007"
                    },
                    "predicate": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#PJkeyword"
                    },
                    "object": {
                        "type": "literal",
                        "value": "Agricultural Water Productivity"
                    },
                    "p_label": {
                        "type": "literal",
                        "value": "Project Keyword"
                    }
                },
                {
                    "subject": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#SET-2009-A007"
                    },
                    "predicate": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#PJdkk"
                    },
                    "object": {
                        "datatype": "http://www.w3.org/2001/XMLSchema#float",
                        "type": "literal",
                        "value": "206000.0"
                    }
                },
                {
                    "subject": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#SET-2009-A007"
                    },
                    "predicate": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#PJstart"
                    },
                    "object": {
                        "datatype": "http://www.w3.org/2001/XMLSchema#dateTime",
                        "type": "literal",
                        "value": "2009-09-01T00:00:00"
                    }
                },
                {
                    "subject": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#SET-2009-A007"
                    },
                    "predicate": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#PJkeyword"
                    },
                    "object": {
                        "type": "literal",
                        "value": "Irrigation Management"
                    },
                    "p_label": {
                        "type": "literal",
                        "value": "Project Keyword"
                    }
                },
                {
                    "subject": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#SET-2009-A007"
                    },
                    "predicate": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#isSponsoredBy"
                    },
                    "object": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#GeologicalSurveyOfDenmarkAndGreenland"
                    }
                },
                {
                    "subject": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#SET-2009-A007"
                    },
                    "predicate": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#isSponsoredBy"
                    },
                    "object": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#FoodAndAgricultureOrganization"
                    },
                    "o_label": {
                        "type": "literal",
                        "value": "FAO"
                    }
                },
                {
                    "subject": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#SET-2009-A007"
                    },
                    "predicate": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#PJContractedAmount"
                    },
                    "object": {
                        "datatype": "http://www.w3.org/2001/XMLSchema#float",
                        "type": "literal",
                        "value": "206000.0"
                    }
                },
                {
                    "subject": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#SET-2009-A007"
                    },
                    "predicate": {
                        "type": "uri",
                        "value": "http://www.semanticweb.org/milkk/ontologies/2017/11/testData#NameOfProject"
                    },
                    "object": {
                        "type": "literal",
                        "value": "PhD Course cum Workshop on Agricultural Water Productivity and Improvement in Irrigation Schemes"
                    }
                }
            ]
        }
    }
    results = main_view.transform_api(test_data)
    new_results = []
    new_results.append(nested_transformation(results, "Thailand"))
    new_results.append(nested_transformation(results, "Vietnam"))

    return render(request, 'pages/timelinegraph.html', {'posts': new_results})


def nested_transformation(results, group):
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

        check_index = next(
            (index for (index, d) in enumerate(new_result['commits']) if d["subject"] == s_label), None)
        if check_index is not None:  # result.get('subject') in new_results['commits'].values()
            tmp = new_result['commits'][check_index]
            tmp[p_label] = o_label
        else:
            tmp = {}
            tmp['subject'] = s_label
            tmp[p_label] = o_label
            new_result['commits'].append(tmp)
    return new_result
