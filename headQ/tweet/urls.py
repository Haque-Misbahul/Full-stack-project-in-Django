from . import views
from django.urls import path

urlpatterns = [
    # path('', views.index, name ='index'),
    path('', views.Tweet_list, name ='tweet_list'),
    path('create/', views.tweet_create, name ='tweet_create'),
    path('<int:tweet_id>/edit/', views.tweet_edit, name ='tweet_edit'),
    path('<int:tweet_id>/delete/', views.tweet_delete, name ='tweet_delete'),
]
