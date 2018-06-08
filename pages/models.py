from django.contrib.postgres.fields import JSONField
from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
import datetime
import os
import json
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from base64 import b64encode

# Create your models here.


def call_api(sparql):
    values = urlencode({'query': 'PREFIX aitslt:<http://www.semanticweb.org/milkk/ontologies/2017/11/testData#>' + sparql})
    credentials = b64encode('admin:admin'.encode('ascii'))
    headers = {
        'Authorization': 'Basic %s' % credentials.decode('ascii'),
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/sparql-results+json'
    }
    data = values.encode('ascii')
    request = Request('http://18.222.54.28:5820/milk-reasoning/query', data=data, headers=headers)
    try:
        response_body = urlopen(request).read().decode('ascii')
        return response_body
    except HTTPError as e:
        print(e.code + e.reason)
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


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    # text = models.TextField()
    graph = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    source = JSONField(blank=True, null=True, editable=False)
    result = JSONField(blank=True, null=True, editable=False)
    facet_country = JSONField(blank=True, null=True, editable=False)
    facet_donor = JSONField(blank=True, null=True, editable=False)
    facet_organizationunit = JSONField(blank=True, null=True, editable=False)
    facet_person = JSONField(blank=True, null=True, editable=False)
    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)

    def save(self, *args, **kwargs):  # do something every time you save
        # if not self.pk:
            # This code only happens if the objects is not in the database yet. Otherwise it would have pk

        #  ex === [{"subject": "ex:ThaiLand", "predicate": "ex:hasFood", "object": "ex:TomYumKung"}]
        #     self.source = [{"subject": "ex:ThaiLand", "predicate": "ex:hasFood", "object": "ex:TomYumKung"},
        #            {"subject": "ex:TomYumKung", "predicate": "ex:isFoodOf", "object": "ex:ThaiLand"},
        #            {"subject": "ex:TomYumKung", "predicate": "rdf:type", "object": "ex:SpicyFood"},
        #            {"subject": "ex:TomYumKung", "predicate": "ex:includes", "object": "ex:shrimp"},
        #            {"subject": "ex:TomYumKung", "predicate": "ex:includes", "object": "ex:chilly"},
        #            {"subject": "ex:TomYumKung", "predicate": "ex:requires", "object": "ex:chilly"},
        #            {'"subject"': "ex:TomYumKung", "predicate": "ex:hasSpicy", "object": "ex:chilly"},
        #            {"subject": "ex:TomYumKung", "predicate": "ex:includes", "object": "ex:lemon"},
        #            {"subject": "ex:lemon", "predicate": "ex:hasTaste", "object": "ex:sour"},
        #            {"subject": "ex:chilly", "predicate": "ex:hasTaste", "object": "ex:spicy"}]

        # {"nodes": [{"id": "hello1"}, {"id": "hello2"}],
        #            "links": [{"source": "hello1", "target": "hello2"}]}

        super().save(*args, **kwargs)  # Call the "real" save() method.

    def publish(self):  # for making publish button on preview page
        self.published_date = timezone.now()
        self.save()

    def was_published_recently(self):
        now = timezone.now()
        if self.published_date is not None:
            return now - datetime.timedelta(days=1) <= self.published_date <= now

    was_published_recently.admin_order_field = 'published_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def __str__(self):
        return self.title


#  -----should be the result from ice API ==> add to DB into "source" attribute-----
@receiver(post_save, sender=Post)
def ensure_post_exists(sender, instance, created, **kwargs):
    # SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    if created is True:  # only new create
        print(instance.subject)
        # json_url = os.path.join(SITE_ROOT, "static/data", "select_project.json")
        # data = json.load(open(json_url))
        sparql_all = 'SELECT DISTINCT * WHERE { ?subject rdf:type aitslt:' + instance.subject + ' .' \
                 + '?subject ?predicate ?object .' \
                 + 'filter(?object != owl:NamedIndividual && ?predicate != rdf:type)' \
                 + '}order by ?subject'
        data = call_api(sparql_all)
        instance.source = json.loads(data)
        #  -----facet country-----
        # json_url = os.path.join(SITE_ROOT, "static/data/facets", "facet_country.json")
        # data = json.load(open(json_url))
        sparql_country = 'select distinct ?object where{?subject rdf:type aitslt:' + instance.subject \
                         + ' . ?subject ?predicate ?object.' \
                         + 'filter(?object != owl:NamedIndividual && ?predicate != rdf:type) ' \
                         + '?object rdf:type aitslt:Country .}order by ?object'
        data = call_api(sparql_country)
        instance.facet_country = json.loads(data)
        #  -----facet donor-----
        # json_url = os.path.join(SITE_ROOT, "static/data/facets", "facet_donor.json")
        # data = json.load(open(json_url))
        sparql_donor = 'select distinct ?donor where{?subject rdf:type aitslt:' + instance.subject \
                       + ' . ?subject ?predicate ?object.' \
                       + 'filter(?object != owl:NamedIndividual && ?predicate != rdf:type) ?object rdf:type ?donor.' \
                       + 'filter(?donor != owl:NamedIndividual && ?predicate = aitslt:isSponsoredBy)' \
                       + '}order by ?donor'
        data = call_api(sparql_donor)
        instance.facet_donor = json.loads(data)
        #  -----facet organization unit-----
        # json_url = os.path.join(SITE_ROOT, "static/data/facets", "facet_organizationunit.json")
        # data = json.load(open(json_url))
        sparql_org = 'select distinct ?organizationunit where{?subject rdf:type aitslt:' + instance.subject \
                     + ' . ?subject ?predicate ?object.' \
                     + 'filter(?object != owl:NamedIndividual && ?predicate != rdf:type) ' \
                     + '?object aitslt:under ?organizationunit .}'
        data = call_api(sparql_org)
        instance.facet_organizationunit = json.loads(data)
        #  -----facet person-----
        # json_url = os.path.join(SITE_ROOT, "static/data/facets", "facet_person.json")
        # data = json.load(open(json_url))
        sparql_person = 'select distinct ?person where{?subject rdf:type aitslt:' + instance.subject \
                        + ' . ?subject ?predicate ?object.' \
                        + 'filter(?object != owl:NamedIndividual && ?predicate != rdf:type) ?object rdf:type ?person.' \
                        + 'filter(?person != owl:NamedIndividual && ( ?predicate = aitslt:includesInvestigator ' \
                        + '|| ?predicate = aitslt:includesMember))}order by ?person'
        data = call_api(sparql_person)
        instance.facet_person = json.loads(data)
        instance.save()
        # print(instance)
    else:
        print(kwargs)
