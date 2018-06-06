from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone
import datetime
import os
import json

# Create your models here.


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


#  -----should be the result from ice API ==> add to DB into "source" attribute-----
    def save(self, *args, **kwargs):
        if not self.pk:  # This code only happens if the objects is not in the database yet. Otherwise it would have pk
            SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
            json_url = os.path.join(SITE_ROOT, "static/data", "select_project.json")
            data = json.load(open(json_url))
            self.source = data
            #  -----facet country-----
            json_url = os.path.join(SITE_ROOT, "static/data/facets", "facet_country.json")
            data = json.load(open(json_url))
            self.facet_country = data
            #  -----facet donor-----
            json_url = os.path.join(SITE_ROOT, "static/data/facets", "facet_donor.json")
            data = json.load(open(json_url))
            self.facet_donor = data
            #  -----facet organization unit-----
            json_url = os.path.join(SITE_ROOT, "static/data/facets", "facet_organizationunit.json")
            data = json.load(open(json_url))
            self.facet_organizationunit = data
            #  -----facet person-----
            # json_url = os.path.join(SITE_ROOT, "static/data/facets", "facet_person.json")
            # data = json.load(open(json_url))
            # self.facet_person = data

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

    def publish(self):
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
