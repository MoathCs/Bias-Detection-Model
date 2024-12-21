from django.db import transaction
from django.core.management.base import BaseCommand
from custom_user.models import Question
import os
import pandas as pd



# from django import pandas as pd


# python manage.py add_question static/cleaned_questions_data.xlsx


class Command(BaseCommand):
    help = 'Imports questions from an Excel file into the database'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Full path to the Excel file')

    def handle(self, *args, **options):
        file_path = options['file_path']
        data = pd.read_excel(file_path)
        with transaction.atomic():
            for index, row in data.iterrows():
                Question.objects.create(
                    right=row['right'],
                    question=row['question']
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported all questions'))




    # def get_questions(selected_rights):
    #     questions = Question.objects.filter(right__in=selected_rights)  # Query questions related to selected rights
    #     print("The Selected Rights:", selected_rights)  # Print selected rights
    #     print("Related Questions:")  # Print related questions (for testing)

    #     for question in questions:
    #         print(question.question)  # Print the question text

    # selected_rights = ['التحرر من الاستعباد','lolo']  # Example list of selected rights
    # get_questions(selected_rights)  # Call the function with the selected rights



# from django.core.management.base import BaseCommand
# from BDM.models import Question

# class Command(BaseCommand):
#     help = 'Prints questions related to selected rights'

#     def add_arguments(self, parser):
#         parser.add_argument('selected_rights', nargs='+', type=str, help='List of selected rights')

#     def handle(self, *args, **options):
#         selected_rights = options['selected_rights']
#         questions = Question.objects.filter(right__in=selected_rights)
#         self.stdout.write(f"The Selected Rights: {selected_rights}")
#         self.stdout.write("Related Questions:")
#         for question in questions:
#             self.stdout.write(question.question)
