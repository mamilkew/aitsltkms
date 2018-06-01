from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone
import datetime

# Create your models here.


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    # text = models.TextField()
    graph = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    result = JSONField(blank=True, null=True, editable=False)
    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)

#  should be the result from ice API
    # def save(self, *args, **kwargs):
    #     self.result = [{"subject": "ex:ThaiLand", "predicate": "ex:hasFood", "object": "ex:TomYumKung"},
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
    # super().save(*args, **kwargs)  # Call the "real" save() method.

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.published_date <= now
    was_published_recently.admin_order_field = 'published_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def __str__(self):
        return self.title
