from django.urls import path

from office_world import views

urlpatterns = [
    path('', views.VoteActiveView.as_view(), name='homepage'),
    path('finished', views.VoteFinishedView.as_view(), name='finished'),
    path(r'current/<slug>/', views.VoteActiveDetailView.as_view(), name='vote-detail'),
    path(r'finished/<slug>/', views.VoteFinishedDetailView.as_view(), name='vote-finish-detail'),
    path(r'vote/<slug>/', views.VoteFormAction.as_view(), name='vote-action'),
]
