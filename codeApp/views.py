from django.db.models import Q
from rest_framework import viewsets,generics
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import LeetcodeProblem
from .serializers import DataEntrySerializer
from django.http import JsonResponse

class LeetcodeProblemViewSet(generics.ListCreateAPIView):
    queryset = LeetcodeProblem.objects.all()
    serializer_class = DataEntrySerializer

class LeetCodeEntryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = LeetcodeProblem.objects.all()
    serializer_class = DataEntrySerializer

def get_filtered_data(self, request):
    problem_id = request.GET.get('problem_id')
    title = request.GET.get('title')
    acceptance = request.GET.get('acceptance')
    difficulty = request.GET.get('difficulty')
    frequency = request.GET.get('frequency')
    company = request.GET.get('company')

    filters = Q()
    if problem_id:
            filters &= Q(problem_id=problem_id)
    if title:
            filters &= Q(title__icontains=title)
    if acceptance:
            filters &= Q(acceptance__icontains=acceptance)
    if difficulty:
            filters &= Q(difficulty__icontains=difficulty)
    if frequency:
            filters &= Q(frequency__lte=float(frequency))
    if company:
            filters &= Q(company__icontains=company)

    data = LeetcodeProblem.objects.filter(filters)
    response_data = [
            {
                "problem_id": item.problem_id,
                "title": item.title,
                "acceptance": item.acceptance,
                "difficulty": item.difficulty,
                "frequency": item.frequency,
                "leetcode_link": item.leetcode_link,
                "company": item.company,
            }
            for item in data
        ]
    return JsonResponse(response_data,safe=False)