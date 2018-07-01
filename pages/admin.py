from dal import autocomplete
from django.contrib import admin
from .models import Post, Postforcegraph, Repository, Forcegraph, Property
from django import forms


# Register your models here.
class ForcegraphForm(forms.ModelForm):
    faceted_search = forms.ModelMultipleChoiceField(queryset=Property.objects.all(),
                                                    widget=autocomplete.ModelSelect2Multiple(url='property_faceted',
                                                                                     forward=('repository_query',
                                                                                              'domain_subject')))

    class Meta:
        model = Forcegraph
        fields = ('__all__')
        ordering = ['property_path']


class PropertyAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Property.objects.none()

        qs = Property.objects.none()

        domain_subject = self.forwarded.get('domain_subject', None)
        if domain_subject:
            qs = Property.objects.filter(domain_prop=domain_subject)

        if self.q:
            qs = Property.objects.filter(domain_prop=domain_subject).filter(property_path__contains=self.q)

        return qs


class ForcegraphAdmin(admin.ModelAdmin):
    form = ForcegraphForm


class RepositoryAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:  # This is the case when obj is already created i.e. it's an edit
            return ['query_path']
        else:
            return []


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'graph', 'subject', 'published_date', 'was_published_recently')
    list_filter = ['published_date']
    search_fields = ['subject', 'result']


class PostforcegraphAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'created_date', 'updated_date', 'was_published_last')
    ordering = ['updated_date']
    list_filter = ['published_date']
    search_fields = ['subject', 'result']


admin.site.register(Repository, RepositoryAdmin)
admin.site.register(Forcegraph, ForcegraphAdmin)
# admin.site.register(Post, PostAdmin)
# admin.site.register(Postforcegraph, PostforcegraphAdmin)
# admin.site.site_header = 'VisualOntology Adminsitration'    # default: "Django Administration"
admin.site.index_title = 'Visualization Management'  # default: "Site administration"
admin.site.site_title = 'VisualOntology site admin'  # default: "Django site admin"
