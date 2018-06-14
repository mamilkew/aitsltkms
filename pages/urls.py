from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # ex: /pages/
    # path('<int:post_id>/', views.detail, name='detail'),  # ex: /pages/5/
    path('filter_detail/', views.filter_detail, name='filter_detail'),
    path('filter_query/', views.filter_query, name='filter_query'),  # for ajax in forcegraph.html
    path('<int:post_id>/', views.forcegraph, name='forcegraph'),
]
