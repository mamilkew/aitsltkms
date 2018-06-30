from django.contrib import admin
from .models import Post, Postforcegraph, Repository, Forcegraph


# Register your models here.
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
admin.site.register(Forcegraph)
# admin.site.register(Post, PostAdmin)
# admin.site.register(Postforcegraph, PostforcegraphAdmin)
# admin.site.site_header = 'VisualOntology Adminsitration'    # default: "Django Administration"
admin.site.index_title = 'Visualization Management'         # default: "Site administration"
admin.site.site_title = 'VisualOntology site admin'         # default: "Django site admin"

