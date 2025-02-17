
from django.urls import path, include
from .views import LeetcodeProblemViewSet,LeetCodeEntryDetail,analyze_code



urlpatterns = [
    path('problems/',LeetcodeProblemViewSet.as_view(),name='leetCodeView'),
    path('problems/<int:pk>',LeetCodeEntryDetail.as_view(),name='Leet-code-entry'),
    path('analyze-code/', analyze_code, name='analyze_code')
] 