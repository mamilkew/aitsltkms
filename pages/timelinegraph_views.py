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
                "object"
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
    new_results = {"name": "Thailand",
                   "commits": []}
    for result in results:
        check_index = next(
            (index for (index, d) in enumerate(new_results['commits']) if d["subject"] == result.get('subject')), None)
        if check_index is not None:  # result.get('subject') in new_results['commits'].values()
            tmp = new_results['commits'][check_index]
            tmp[result.get('predicate')] = result.get('object')
            # new_results[check_index].append(tmp)
        else:
            tmp = {}
            tmp['subject'] = result.get('subject')
            tmp[result.get('predicate')] = result.get('object')
            new_results['commits'].append(tmp)

    return render(request, 'pages/timelinegraph.html', {'posts': [new_results]})
