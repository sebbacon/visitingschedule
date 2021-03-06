from datetime import date

from django.db import models
from django.urls import reverse


class Helper(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, primary_key=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('helper-detail', kwargs={'helper': self.pk})


class Event(models.Model):
    SLOT_CHOICES = (
        ('MORNING', 'am'),
        ('EVENING', 'pm'),
    )
    helpers = models.ManyToManyField(
        Helper, blank=True)
    date = models.DateField()
    slot = models.CharField(choices=SLOT_CHOICES, max_length=12)

    def __str__(self):
        if self.helpers:
            filled_str = "filled by {}".format(",".join([str(h) for h in self.helpers.all()]))
        else:
            filled_str = "currently unfilled"
        return "{} slot on {} {}".format(self.slot, self.date, filled_str)

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk': self.pk})

    def events_on_same_day(self):
        return Event.objects.filter(date=self.date)

    @property
    def klasses(self):
        klasses = []
        if self.is_sunday:
            klasses.append("sunday")
        if self.date < date.today():
            klasses.append("past")
        if self.date == date.today():
            klasses.append("today")
        if all([x.helpers.count() > 0 for x in self.events_on_same_day()]):
            klasses.append("full")
        if all([not x.helpers.count() > 0 for x in self.events_on_same_day()]):
            klasses.append("empty")
        return " ".join(klasses)

    @property
    def is_sunday(self):
        return self.date.weekday() == 6
