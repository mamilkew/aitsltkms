from django.urls import path
from . import views, forcegraph_views, timelinegraph_views

urlpatterns = [
    path('', views.index, name='index'),  # ex: /pages/
    path('detail/<int:post_id>/', views.detail, name='detail'),  # ex: /pages/5/
    path('filter_detail/', views.filter_detail, name='filter_detail'),

    path('<int:post_id>/', forcegraph_views.forcegraph, name='forcegraph'),
    path('filter_query/', forcegraph_views.filter_query, name='filter_query'),  # for ajax in forcegraph.html

    path('filter_timeline/', timelinegraph_views.filter_timeline, name='filter_timeline'),
    path('timeline/', timelinegraph_views.timelinegraph, name='timelinegraph'),
]
