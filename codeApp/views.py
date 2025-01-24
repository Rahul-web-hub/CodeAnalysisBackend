from django.db.models import Q
from rest_framework import viewsets,generics
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import LeetcodeProblem
from .serializers import DataEntrySerializer
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework import serializers, status


# Serializer for registration
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

# View for registration
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PrivateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "You have access!"})


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