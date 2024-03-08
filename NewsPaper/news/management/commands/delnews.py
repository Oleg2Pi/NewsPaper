from typing import Any
from django.core.management.base import BaseCommand, CommandError, CommandParser
from news.models import Post, Category

class Command(BaseCommand):
    help = 'Удалить все созданные статьи'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('category', type=str)

    def handle(self, *args: Any, **options: Any) -> str | None:
        answer = input(f'Вы прадва хотите удалить все статьи в категории {options["category"]}? yes/no\n')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))
            return
        try:
            category = Category.objects.get(name=options['category'])
            Post.objects.filter(category=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Succesfully deleted all news from category {category.name}'))
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Could not find category {options["category"]}'))