import os
import django
import json
from django.db import transaction
from codeApp.models import LeetcodeProblem

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CodeAnalysis.settings")
django.setup()

def load_data():
    # Path to your JSON file
    json_file_path = os.path.join('data', 'data.json')

    try:
        
        with open(json_file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"File {json_file_path} not found.")
        return
    except json.JSONDecodeError:
        print(f"Error parsing JSON file: {json_file_path}")
        return

    # Collect data for bulk creation or updating
    bulk_data = []
    
    with transaction.atomic():
        for item in data:
            bulk_data.append(LeetcodeProblem(
                problem_id=item['ID'],
                title=item['Title'],
                acceptance=item['Acceptance'],
                difficulty=item['Difficulty'],
                frequency=item['Frequency'],
                leetcode_link=item['Leetcode Question Link'].strip(),
                company=item['Company']
            ))

        # Bulk create objects (note: this will not handle updates)
        LeetcodeProblem.objects.bulk_create(bulk_data, ignore_conflicts=True)

        # Alternatively, handle updates in a different way (updating in batches)
        for item in data:
            LeetcodeProblem.objects.filter(problem_id=item['ID']).update(
                title=item['Title'],
                acceptance=item['Acceptance'],
                difficulty=item['Difficulty'],
                frequency=item['Frequency'],
                leetcode_link=item['Leetcode Question Link'].strip(),
                company=item['Company']
            )

    print("Data loaded successfully!")

if __name__ == "__main__":
    load_data()
