from django.core.management.base import BaseCommand
from django_q.tasks import schedule

class Command(BaseCommand):
    help = 'Schedule the auto-cancellation task'

    def handle(self, *args, **options):
        schedule(
            'dashboard.tasks.cancel_overdue_reservations',
            schedule_type='I',  # Interval
            minutes=1,
            repeats=-1  # Repeat indefinitely
        )
        self.stdout.write('Scheduled auto-cancellation task')