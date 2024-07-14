from django.urls import path

from . import views

app_name = 'news'

urlpatterns = [
    path('news_list/', views.news_list, name='news_list'),
    path(
        'comments_count_field/<pk>/',
        views.comments_count_field,
        name='comments_count_field',
    ),
    path('more/<pk>/', views.more, name='more'),
    path('news_create/', views.news_create, name='news_create'),
    path('news_edit/<pk>/', views.news_edit, name='news_edit'),
    path('news_delete/<pk>/', views.news_delete, name='news_delete'),
]
