

from django.conf.urls import url,patterns
from views import *


urlpatterns = [
      url(r'^testStart/$', testStart),
      url(r'^testStop/$', testStop)
]

