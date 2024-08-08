
from django.urls import path, include
from .views import LeetcodeProblemViewSet,LeetCodeEntryDetail



urlpatterns = [
    path('problems/',LeetcodeProblemViewSet.as_view(),name='leetCodeView'),
    path('problems/<int:pk>',LeetCodeEntryDetail.as_view(),name='Leet-code-entry'),
]