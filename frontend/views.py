from urllib.parse import unquote
from datetime import date
from datetime import timedelta

from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import UpdateView

from django_ajax.decorators import ajax

from frontend.models import Event
from frontend.models import Helper


@ajax
def claim_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    helper = get_object_or_404(Helper, pk=request.session['helper'])
    event.helpers.add(helper)
    event.save()
    resp = '%s <a class="adder" href="/event/%s/unclaim"><span class="delete"><img src="/static/cross.svg" height="12px" alt="remove yourself from this slot"></span></a>' % (helper.name, event.pk)
    return resp


@ajax
def unclaim_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.helpers.remove(request.session['helper'])
    event.save()
    resp = '<a class="adder" href="/event/%s/claim"><img src="/static/tick.svg" height="12px" alt="add yourself to this slot"></a>' % event.pk
    return resp


def claim_helper(request, helper):
    request.session['helper'] = helper
    return redirect('event-list')


def logout_helper(request):
    del(request.session['helper'])
    return redirect('event-list')


def get_most_recent_monday():
    start_day = date.today()
    day_of_week = start_day.weekday()
    while day_of_week != 0:
        start_day = start_day - timedelta(days=1)
        day_of_week = start_day.weekday()
    return start_day


class EventList(ListView):
    model = Event

    def get_queryset(self):
        start_day = get_most_recent_monday()
        events = Event.objects.filter(date__gte=start_day, slot='MORNING')
        return events


class HelperEventList(ListView):
    template_name = 'frontend/event_list_schedule.html'

    def get_queryset(self):
        start_day = get_most_recent_monday()
        return Event.objects.filter(
            date__gte=start_day, helpers=self.kwargs['helper'])


class HelperList(ListView):
    model = Helper

    def get_queryset(self):
        self.helper = self.kwargs.get('helper', None)
        if self.helper:
            Helper.objects.filter(pk=self.helper)
        else:
            return Helper.objects.all()


class HelperCreate(CreateView):
    model = Helper
    fields = ['name', 'email']

    def form_valid(self, form):
        claim_helper(self.request, form.data['email'])
        return super().form_valid(form)


class HelperUpdate(UpdateView):
    model = Helper
    fields = ['name', 'email']


class HelperDelete(DeleteView):
    model = Helper
    success_url = reverse_lazy('helper-list')


class HelperDetailView(DetailView):

    queryset = Helper.objects.all()


class EventUpdate(UpdateView):
    model = Event
    fields = ['helper']
