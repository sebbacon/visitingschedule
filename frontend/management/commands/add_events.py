from django.core.management.base import BaseCommand
from frontend.models import Event
import django.db
from datetime import timedelta, date
from frontend.views import get_most_recent_monday


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


class Command(BaseCommand):
    """
    Regular task.
    """
    def handle(self, *args, **options):
        day = get_most_recent_monday()
        for day in daterange(day, day + timedelta(days=49)):
            for slot in [x[0] for x in Event.SLOT_CHOICES]:
                Event.objects.create(
                    date=day,
                    slot=slot
                )
