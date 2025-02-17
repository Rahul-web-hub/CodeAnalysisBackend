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
from django.core.cache import cache
import requests
import hashlib 
import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from anthropic import Anthropic
import os
from django.conf import settings
import time
import re



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

@csrf_exempt
def analyze_code(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            code = data.get("code", "")

            if not code:
                return JsonResponse({"error": "No code provided"}, status=400)

            headers = {
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "your-site-url",
                "X-Title": "your-site-name"
            }

            # **Force AI to return valid JSON**
            prompt = f"""
            You are an AI code reviewer. Analyze the following  code and return a JSON response evaluating:
            1. **Time and space complexity** (Big-O notation with explanation).
            2. **Code quality** (Rate 0-100 based on clarity and best practices).
            3. **Optimization suggestions** (Ways to improve performance).
            4. **Recognized patterns** (Algorithms, techniques, or structures used).

            **Output format (strictly return only this JSON, no extra text):**
            {{
                "complexity": {{
                    "time": "O(n log n)",
                    "space": "O(1)",
                    "explanation": "Sorting algorithm complexity."
                }},
                "quality": {{
                    "score": 85,
                    "issues": ["Use meaningful variable names", "Avoid deeply nested loops"]
                }},
                "optimization": ["Use dictionary lookup instead of list iteration"],
                "patterns": ["Greedy Algorithm", "Sorting"]
            }}

            Now analyze this code:
            ```
            {code}
            ```
            **Do not return anything outside the JSON format. No extra text.**
            """

            payload = {
                "model": "cognitivecomputations/dolphin3.0-mistral-24b:free",
                "messages": [
                    {"role": "system", "content": "You are an AI code reviewer. Strictly return JSON."},
                    {"role": "user", "content": prompt}
                ]
            }

            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)

            if response.status_code == 200:
                response_data = response.json()
                ai_message = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")

                # **Regex to extract JSON if AI includes extra text**
                match = re.search(r"\{.*\}", ai_message, re.DOTALL)
                if match:
                    ai_message = match.group(0)  # Extract the JSON part

                # **Ensure the AI response is valid JSON**
                try:
                    structured_response = json.loads(ai_message)
                    return JsonResponse(structured_response)
                except json.JSONDecodeError:
                    return JsonResponse({"error": "AI response was not in valid JSON format"}, status=500)

            return JsonResponse({"error": "Failed to fetch AI response"}, status=500)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)

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