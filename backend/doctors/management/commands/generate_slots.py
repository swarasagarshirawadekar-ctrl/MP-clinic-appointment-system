from datetime import date, datetime, timedelta
from django.core.management.base import BaseCommand
from doctors.models import Availability, Slot


class Command(BaseCommand):
    help = "Generate slots for the next 7 days from Availability rules"

    def handle(self, *args, **options):
        created_count = 0
        today = date.today()

        for availability in Availability.objects.all():
            for day_offset in range(7):
                current_date = today + timedelta(days=day_offset)

                # only continue if this date's weekday matches the rule (e.g. Monday)
                if current_date.strftime("%A").lower() != availability.weekday.strip().lower():
                    continue

                start = datetime.combine(current_date, availability.start_time)
                end = datetime.combine(current_date, availability.end_time)
                step = timedelta(minutes=availability.slot_length_minutes)

                # keep cutting slots until the availability window is full
                while start + step <= end:
                    slot, created = Slot.objects.get_or_create(
                        availability=availability,
                        date=current_date,
                        start_time=start.time(),
                        end_time=(start + step).time(),
                    )
                    if created:
                        created_count += 1
                    start += step

        self.stdout.write(self.style.SUCCESS(f"{created_count} slots created"))