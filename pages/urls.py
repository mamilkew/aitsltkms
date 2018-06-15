from django.urls import path
from . import views, forcegraph_views

urlpatterns = [
    path('', views.index, name='index'),  # ex: /pages/
    path('detail/<int:post_id>/', views.detail, name='detail'),  # ex: /pages/5/
    path('filter_detail/', views.filter_detail, name='filter_detail'),
    path('<int:post_id>/', forcegraph_views.forcegraph, name='forcegraph'),
    path('filter_query/', forcegraph_views.filter_query, name='filter_query'),  # for ajax in forcegraph.html
]
