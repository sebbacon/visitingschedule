"""visitingschedule URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import path
from django.urls import reverse_lazy
from django.contrib import admin

from frontend.views import EventList
from frontend.views import EventUpdate
from frontend.views import HelperCreate
from frontend.views import HelperDelete
from frontend.views import HelperUpdate
from frontend.views import HelperList
from frontend.views import HelperDetailView
from frontend.views import claim_event
from frontend.views import unclaim_event
from frontend.views import claim_helper
from frontend.views import logout_helper


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('events/', EventList.as_view(), name='event-list'),
    path('event/<int:pk>/', EventUpdate.as_view(), name='event-update'),
    path('event/<int:pk>/claim', claim_event, name='event-claim'),
    path('event/<int:pk>/unclaim', unclaim_event, name='event-unclaim'),
    path('helper/<str:pk>/claim', claim_helper, name='helper-claim'),
    path('helper/logout', logout_helper, name='helper-logout'),
    path('helpers/', HelperList.as_view(), name='helper-list'),
    path('helper/add/',
         HelperCreate.as_view(success_url=reverse_lazy('event-list')),
         name='helper-add', ),
    path('helper/<str:pk>/edit', HelperUpdate.as_view(), name='helper-update'),
    path('helper/<str:pk>/', HelperDetailView.as_view(), name='helper-detail'),
    path('helper/<str:pk>/delete/', HelperDelete.as_view(), name='helper-delete'),
]
