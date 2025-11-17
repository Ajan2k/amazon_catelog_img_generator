from django.core.management.base import BaseCommand
from products.models import Template
from generation.templates import TEMPLATES


class Command(BaseCommand):
    help = 'Initialize default templates'

    def handle(self, *args, **kwargs):
        for key, spec in TEMPLATES.items():
            template, created = Template.objects.get_or_create(
                name=spec['name'],
                defaults={
                    'kind': spec['kind'],
                    'spec': spec,
                    'is_active': True,
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created template: {template.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Template already exists: {template.name}')
                )
        
        self.stdout.write(self.style.SUCCESS('Templates initialization complete!'))