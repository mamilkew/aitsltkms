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
from django.db.models import Q
from smart_selects.db_fields import ChainedForeignKey, ChainedManyToManyField
from pages import extractor_transformation as extractor_trans


# Create your models here.
class Repository(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    repo_name = models.CharField(max_length=200)
    query_path = models.URLField(max_length=500)
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    updated_date = models.DateTimeField(blank=True, editable=False)

    class Meta:
        verbose_name = 'My Repository'
        verbose_name_plural = 'My Repositories'

    def save(self, *args, **kwargs):  # do something every time you save
        self.updated_date = timezone.now()
        super().save(*args, **kwargs)  # Call the "real" save() method.

    def __str__(self):
        return '%s <%s>' % (self.repo_name, self.query_path)

    # class Meta:
    #     verbose_name = 'My Repository'
    #     verbose_name_plural = 'My Repositories'


def save_repository(sender, instance, created, **kwargs):
    if created:
        sparql_class = 'SELECT DISTINCT ?class ?c_label ' \
                       + 'WHERE {' \
                       + '?property rdfs:domain ?class .' \
                       + 'optional{?class rdfs:label ?c_label}' \
                       + '}order by ?class'
        data_class = call_api(sparql_class, instance.query_path)
        results = json.loads(data_class)
        for result in results['results']['bindings']:
            Domain.objects.create(domain_path=result.get('class').get('value'), author_id=instance.author_id,
                                  repository_query=instance)

        sparql_property = 'SELECT DISTINCT ?class ?c_label ?property ?p_label ' \
                          + 'WHERE {' \
                          + '?property rdfs:domain ?class .' \
                          + 'optional{?class rdfs:label ?c_label}' \
                          + 'optional{?property rdfs:label ?p_label}' \
                          + '}order by ?class'
        data_property = call_api(sparql_property, instance.query_path)
        results = json.loads(data_property)
        for result in results['results']['bindings']:
            check_class = Domain.objects.filter(repository_query=instance.id).filter(
                domain_path=result.get('class').get('value')).first()
            Property.objects.create(property_path=result.get('property').get('value'), author_id=instance.author_id,
                                    domain_prop=check_class, repository_query=instance)


post_save.connect(save_repository, sender=Repository)


class Domain(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    domain_path = models.URLField(max_length=500)
    repository_query = models.ForeignKey(Repository, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.domain_path


class Property(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    property_path = models.URLField(max_length=500)
    domain_prop = models.ForeignKey(Domain, on_delete=models.CASCADE, blank=True, null=True)
    repository_query = models.ForeignKey(Repository, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.property_path


class Forcegraph(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    page_title = models.CharField(max_length=200)
    repository_query = models.ForeignKey(Repository, on_delete=models.CASCADE)
    domain_subject = ChainedForeignKey(
        Domain,
        chained_field='repository_query',
        chained_model_field='repository_query',
        show_all=False,
        auto_choose=True,
        sort=True
    )
    faceted_search = models.ManyToManyField(Property)
    # domain_subject = models.ForeignKey(Domain, on_delete=models.CASCADE)
    source = JSONField(blank=True, null=True, editable=False)
    result = JSONField(blank=True, null=True, editable=False)
    created_date = models.DateTimeField(
        default=timezone.now, editable=False)
    updated_date = models.DateTimeField(
        default=timezone.now, editable=False)
    published_date = models.DateTimeField(
        blank=True, null=True)

    class Meta:
        verbose_name = 'Graph Node-Link'
        verbose_name_plural = 'Graph Node-Links'

    def save(self, *args, **kwargs):  # do something every time you save
        if not self.pk:
            sparql_all = 'SELECT DISTINCT * WHERE { ?subject rdf:type <' + self.domain_subject.domain_path + '> .' \
                         + '?subject ?predicate ?object .' \
                         + 'optional{?subject rdfs:label ?s_label}' \
                         + 'optional{?predicate rdfs:label ?p_label}' \
                         + 'optional{?object rdfs:label ?o_label}' \
                         + 'filter(?object != owl:NamedIndividual)' \
                         + '}order by ?subject'  # filter(?object != owl:NamedIndividual && ?predicate != rdf:type)
            data = call_api(sparql_all, self.repository_query.query_path)
            self.source = json.loads(data)
            self.result = extractor_trans.transform_api(json.loads(data))  # solve the problem of saving frequently
            self.updated_date = timezone.now()
            super().save(*args, **kwargs)  # Call the "real" save() method.
        else:
            self.updated_date = timezone.now()
            super().save(*args, **kwargs)  # Call the "real" save() method.

    def was_published_last(self):
        now = timezone.now()
        if self.published_date is not None:
            return self.published_date <= now

    was_published_last.admin_order_field = 'published_date'
    was_published_last.boolean = True
    was_published_last.short_description = 'Published ?'

    def __str__(self):
        return self.page_title


class Timelinegraph(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    page_title = models.CharField(max_length=200)
    repository_query = models.ForeignKey(Repository, on_delete=models.CASCADE)
    domain_subject = ChainedForeignKey(
        Domain,
        chained_field='repository_query',
        chained_model_field='repository_query',
        show_all=False,
        auto_choose=True,
        sort=True
    )
    date_marked = models.ForeignKey(Property, on_delete=models.CASCADE)
    # date_marked = ChainedForeignKey(
    #     Property,
    #     chained_field='domain_subject',
    #     chained_model_field='domain_prop',
    #     # related_name='date_marked',
    #     show_all=False,
    #     auto_choose=False,
    #     sort=True
    # )
    faceted_search = models.ManyToManyField(Property, related_name='faceted_search')
    # domain_subject = models.ForeignKey(Domain, on_delete=models.CASCADE)
    source = JSONField(blank=True, null=True, editable=False)
    result = JSONField(blank=True, null=True, editable=False)
    created_date = models.DateTimeField(
        default=timezone.now, editable=False)
    updated_date = models.DateTimeField(
        default=timezone.now, editable=False)
    published_date = models.DateTimeField(
        blank=True, null=True)

    class Meta:
        verbose_name = 'Graph Timeline'
        verbose_name_plural = 'Graph Timelines'

    def save(self, *args, **kwargs):  # do something every time you save
        if not self.pk:
            sparql_all = 'SELECT DISTINCT * WHERE { ?subject rdf:type <' + self.domain_subject.domain_path + '> .' \
                         + '?subject ?predicate ?object .' \
                         + 'optional{?subject rdfs:label ?s_label}' \
                         + 'optional{?predicate rdfs:label ?p_label}' \
                         + 'optional{?object rdfs:label ?o_label}' \
                         + 'filter(?object != owl:NamedIndividual)' \
                         + '}order by ?subject'  # filter(?object != owl:NamedIndividual && ?predicate != rdf:type)
            data = call_api(sparql_all, self.repository_query.query_path)
            self.source = json.loads(data)
            results = extractor_trans.transform_api(json.loads(data))
            new_results = []
            new_results.append(extractor_trans.nested_transformation(results, "All",
                                                                     self.date_marked.property_path.split('#')[-1]))
            self.result = new_results  # solve the problem of saving frequently
            self.updated_date = timezone.now()
            super().save(*args, **kwargs)  # Call the "real" save() method.
        else:
            self.updated_date = timezone.now()
            super().save(*args, **kwargs)  # Call the "real" save() method.

    def was_published_last(self):
        now = timezone.now()
        if self.published_date is not None:
            return self.published_date <= now

    was_published_last.admin_order_field = 'published_date'
    was_published_last.boolean = True
    was_published_last.short_description = 'Published ?'

    def __str__(self):
        return self.page_title


def call_api(sparql, link_query):
    values = urlencode(
        {'query': 'PREFIX aitslt:<http://www.semanticweb.org/milkk/ontologies/2017/11/testData#>' + sparql})
    credentials = b64encode('admin:admin'.encode('ascii'))
    headers = {
        'Authorization': 'Basic %s' % credentials.decode('ascii'),
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/sparql-results+json'
    }
    data = values.encode('ascii')
    request = Request(link_query, data=data, headers=headers)
    try:
        response_body = urlopen(request).read().decode('utf8')
        return response_body
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


class Postforcegraph(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    subject = models.URLField(max_length=200)
    source = JSONField(blank=True, null=True, editable=False)
    result = JSONField(blank=True, null=True, editable=False)
    created_date = models.DateTimeField(
        default=timezone.now, editable=False)
    updated_date = models.DateTimeField(
        default=timezone.now, editable=False)
    published_date = models.DateTimeField(
        blank=True, null=True)

    def save(self, *args, **kwargs):  # do something every time you save
        sparql_all = 'SELECT DISTINCT * WHERE { ?subject rdf:type <' + self.subject + '> .' \
                     + '?subject ?predicate ?object .' \
                     + 'optional{?subject rdfs:label ?s_label}' \
                     + 'optional{?predicate rdfs:label ?p_label}' \
                     + 'optional{?object rdfs:label ?o_label}' \
                     + 'filter(?object != owl:NamedIndividual)' \
                     + '}order by ?subject'  # filter(?object != owl:NamedIndividual && ?predicate != rdf:type)
        data = call_api(sparql_all, 'http://18.222.54.28:5820/milk-reasoning/query')
        self.source = json.loads(data)
        self.updated_date = timezone.now()
        super().save(*args, **kwargs)  # Call the "real" save() method.

    def was_published_last(self):
        now = timezone.now()
        if self.published_date is not None:
            return self.published_date <= now

    was_published_last.admin_order_field = 'published_date'
    was_published_last.boolean = True
    was_published_last.short_description = 'Last Published ?'

    def __str__(self):
        return self.title


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
        sparql_all = 'SELECT DISTINCT * WHERE { ?subject rdf:type aitslt:' + self.subject + ' .' \
                     + '?subject ?predicate ?object .' \
                     + 'filter(?object != owl:NamedIndividual)' \
                     + '}order by ?subject'  # filter(?object != owl:NamedIndividual && ?predicate != rdf:type
        data = call_api(sparql_all, 'http://18.222.54.28:5820/milk-reasoning/query')
        self.source = json.loads(data)
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


# -----should be the result from ice API ==> add to DB into "source" attribute-----
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
        data = call_api(sparql_all, 'http://18.222.54.28:5820/milk-reasoning/query')
        instance.source = json.loads(data)
        #  -----facet country-----
        # json_url = os.path.join(SITE_ROOT, "static/data/facets", "facet_country.json")
        # data = json.load(open(json_url))
        sparql_country = 'select distinct ?object where{?subject rdf:type aitslt:' + instance.subject \
                         + ' . ?subject ?predicate ?object.' \
                         + 'filter(?object != owl:NamedIndividual && ?predicate != rdf:type) ' \
                         + '?object rdf:type aitslt:Country .}order by ?object'
        data = call_api(sparql_country, 'http://18.222.54.28:5820/milk-reasoning/query')
        instance.facet_country = json.loads(data)
        #  -----facet donor-----
        # json_url = os.path.join(SITE_ROOT, "static/data/facets", "facet_donor.json")
        # data = json.load(open(json_url))
        sparql_donor = 'select distinct ?donor where{?subject rdf:type aitslt:' + instance.subject \
                       + ' . ?subject ?predicate ?object.' \
                       + 'filter(?object != owl:NamedIndividual && ?predicate != rdf:type) ?object rdf:type ?donor.' \
                       + 'filter(?donor != owl:NamedIndividual && ?predicate = aitslt:isSponsoredBy)' \
                       + '}order by ?donor'
        data = call_api(sparql_donor, 'http://18.222.54.28:5820/milk-reasoning/query')
        instance.facet_donor = json.loads(data)
        #  -----facet organization unit-----
        # json_url = os.path.join(SITE_ROOT, "static/data/facets", "facet_organizationunit.json")
        # data = json.load(open(json_url))
        sparql_org = 'select distinct ?organizationunit where{?subject rdf:type aitslt:' + instance.subject \
                     + ' . ?subject ?predicate ?object.' \
                     + 'filter(?object != owl:NamedIndividual && ?predicate != rdf:type) ' \
                     + '?object aitslt:under ?organizationunit .}'
        data = call_api(sparql_org, 'http://18.222.54.28:5820/milk-reasoning/query')
        instance.facet_organizationunit = json.loads(data)
        #  -----facet person-----
        # json_url = os.path.join(SITE_ROOT, "static/data/facets", "facet_person.json")
        # data = json.load(open(json_url))
        sparql_person = 'select distinct ?person where{?subject rdf:type aitslt:' + instance.subject \
                        + ' . ?subject ?predicate ?object.' \
                        + 'filter(?object != owl:NamedIndividual && ?predicate != rdf:type) ?object rdf:type ?person.' \
                        + 'filter(?person != owl:NamedIndividual && ( ?predicate = aitslt:includesInvestigator ' \
                        + '|| ?predicate = aitslt:includesMember))}order by ?person'
        data = call_api(sparql_person, 'http://18.222.54.28:5820/milk-reasoning/query')
        instance.facet_person = json.loads(data)
        instance.save()
        # print(instance)
    else:
        print(kwargs)
