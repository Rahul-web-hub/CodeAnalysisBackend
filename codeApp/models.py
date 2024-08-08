from django.db import models

class LeetcodeProblem(models.Model):
    problem_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    acceptance = models.CharField(max_length=10)
    difficulty = models.CharField(max_length=10)
    frequency = models.FloatField()
    leetcode_link = models.URLField()
    company = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.problem_id}: {self.title}"