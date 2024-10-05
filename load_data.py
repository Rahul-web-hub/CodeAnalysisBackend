import os
import django
import json
from django.db import transaction
from codeApp.models import LeetcodeProblem

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CodeAnalysis.settings")
django.setup()

def load_data():
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

    bulk_data = []
    update_data = []
    existing_problem_ids = set(LeetcodeProblem.objects.values_list('problem_id', flat=True))

    with transaction.atomic():
        for item in data:
            if item['ID'] in existing_problem_ids:
                update_data.append(LeetcodeProblem(
                    problem_id=item['ID'],
                    title=item['Title'],
                    acceptance=item['Acceptance'],
                    difficulty=item['Difficulty'],
                    frequency=item['Frequency'],
                    leetcode_link=item['Leetcode Question Link'].strip(),
                    company=item['Company']
                ))
            else:
                bulk_data.append(LeetcodeProblem(
                    problem_id=item['ID'],
                    title=item['Title'],
                    acceptance=item['Acceptance'],
                    difficulty=item['Difficulty'],
                    frequency=item['Frequency'],
                    leetcode_link=item['Leetcode Question Link'].strip(),
                    company=item['Company']
                ))

        # Bulk create new objects
        if bulk_data:
            LeetcodeProblem.objects.bulk_create(bulk_data, ignore_conflicts=True)

        # Bulk update existing objects
        if update_data:
            LeetcodeProblem.objects.bulk_update(update_data, ['title', 'acceptance', 'difficulty', 'frequency', 'leetcode_link', 'company'])

    print("Data loaded successfully!")

if __name__ == "__main__":
    load_data()
