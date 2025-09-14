from django.urls import path
from . import views

urlpatterns = [
    path('', views.random_quote_view, name='random_quote'),
    path('quote/<int:quote_id>/like/', views.like, name='like_quote'),
    path('quote/<int:quote_id>/dislike/', views.dislike, name='dislike_quote'),
]
