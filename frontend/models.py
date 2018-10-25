from django.db import models
from django.urls import reverse


class Helper(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, primary_key=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('helper-detail', kwargs={'pk': self.pk})


class Event(models.Model):
    SLOT_CHOICES = (
        ('MORNING', 'Morning commute'),
        ('EVENING', 'Evening commute'),
        ('DINNER', 'Dinner'),
    )
    helper = models.ForeignKey(
        Helper, blank=True, null=True, on_delete=models.SET_NULL)
    date = models.DateField()
    slot = models.CharField(choices=SLOT_CHOICES, max_length=12)

    def __str__(self):
        if self.helper:
            filled_str = "filled by {}".format(self.helper)
        else:
            filled_str = "currently unfilled"
        return "{} slot on {} {}".format(self.slot, self.date, filled_str)

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk': self.pk})