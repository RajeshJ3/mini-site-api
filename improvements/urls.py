from django.urls import path
from improvements import views

urlpatterns = [
    path('creators/', views.CreatorViewSet.as_view()),
    path('entries/', views.EntryViewSet.as_view()),
]