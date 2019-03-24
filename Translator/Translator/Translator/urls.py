"""
Definition of urls for Translator.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views



urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^pdf', app.views.pdf, name='pdf'),
    url(r'^image', app.views.image, name='image'),
   

]
