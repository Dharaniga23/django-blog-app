from blog.models import Category
from typing import Any
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "This command inserts post data"

    def handle(self, *args: Any, **options: Any):
         #delete existing data
         Category.objects.all().delete()
         
         categories = ['Sports', 'Technology', 'Travel', 'Food', 'Education']
                    
         for category_name in categories:
                Category.objects.create(name = category_name)
    
         self.stdout.write(self.style.SUCCESS("Category data inserted successfully"))