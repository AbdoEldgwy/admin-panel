from django.core.management.base import BaseCommand
from questions.models import Label

class Command(BaseCommand):
    help = 'Initialize labels from constants'
 
    def handle(self, *args, **kwargs):
        self.stdout.write('Initializing labels...')
        Label.initialize_labels()
        self.stdout.write(self.style.SUCCESS('Successfully initialized labels')) 