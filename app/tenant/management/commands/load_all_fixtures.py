import os

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Load all fixtures from the app'

    def handle(self, *args, **kwargs):
        fixture_dirs = [
            os.path.join('tenant', 'fixtures'),
            os.path.join('task', 'fixtures'),
        ]
        for fixture_dir in fixture_dirs:
            for filename in os.listdir(fixture_dir):
                if filename.endswith('.json'):
                    self.stdout.write(f'Loading {filename}...')
                    call_command('loaddata', os.path.join(fixture_dir, filename))
        self.stdout.write(self.style.SUCCESS('All fixtures loaded successfully.'))
