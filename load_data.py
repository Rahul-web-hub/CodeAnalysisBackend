import os
import django
import json

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CodeAnalysis.settings")
django.setup()

# Now you can import your models
from codeApp.models import LeetcodeProblem

def load_data():
    # Path to your JSON file
    json_file_path = 'data\\data.json'

    # Read the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Iterate through the data and create or update LeetCodeProblem objects
    for item in data:
        LeetcodeProblem.objects.update_or_create(
            problem_id=item['ID'],
            defaults={
                'title': item['Title'],
                'acceptance': item['Acceptance'],
                'difficulty': item['Difficulty'],
                'frequency': item['Frequency'],
                'leetcode_link': item['Leetcode Question Link'].strip(),
                'company':item['Company'],
            }
        )

    print("Data loaded successfully!")

if __name__ == "__main__":
    load_data()