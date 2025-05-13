from django.contrib import admin
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('created_by/<int:author_id>', views.CreatedByListView.as_view(), name='created_by'),
    path('post/<slug:slug>/', views.post, name='post'),
    path('page/', views.page, name='page'),
    path('category/<slug:slug>', views.category, name='category'),
    path('tag/<slug:slug>', views.tag, name='tag'),
    path('search/', views.search, name='search'),
]



