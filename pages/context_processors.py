from django.utils import timezone
from django.db.models import Avg, Count, Min, Max, Sum


def navbarmain(request):
    # from pages.models import Postforcegraph
    from pages.models import Forcegraph
    raw_query = "SELECT DISTINCT ON (page_title) " \
                "*, max(published_date) FROM pages_forcegraph " \
                "WHERE published_date is not null " \
                "GROUP BY page_title, id " \
                "ORDER BY page_title ASC, published_date DESC"

    # raw_query = "SELECT DISTINCT ON (subject) *, max(published_date) FROM pages_postforcegraph WHERE published_date is not null GROUP BY subject, id ORDER BY subject ASC , published_date DESC"
    # for p in Post.objects.raw(raw_query):
    #     print(p)
    # pb = Post.objects.values('subject').annotate(newest_published_date=Max('published_date'))
    # pb_list = Post.objects.filter(subject__in=[b.get('subject') for b in pb], published_date__in=[b.get('newest_published_date') for b in pb])
    # print(pb_list)

    from pages.models import Timelinegraph
    timeline_bar = Timelinegraph.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    return {'navbarMain': Forcegraph.objects.raw(raw_query), 'navbar_timeline': timeline_bar}
