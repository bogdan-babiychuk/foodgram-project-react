from django.core.management.base import BaseCommand
from recipe.models import Ingredient
import csv


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        data_path = 'data/ingredients.csv'

        try:
            with open(data_path, 'r', encoding='utf-8') as csvfile:
                csv_reader = csv.reader(csvfile)

                ingredients = [
                    Ingredient.objects.get_or_create(name=row[0],
                                                     units=row[1])[0]
                    for row in csv_reader if row[0]
                ]
                Ingredient.objects.bulk_create(ingredients,
                                               ignore_conflicts=True)

            self.stdout.write(self.style.SUCCESS(
                'Ингредиенты добавлены'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('CSV файл не найден.'))
