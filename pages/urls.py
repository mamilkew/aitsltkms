from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # ex: /pages/
    path('<int:post_id>/', views.detail, name='detail'),  # ex: /pages/5/
]
