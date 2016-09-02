from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^welcome/', views.welcome, name='welcome'),
    url(r'^topic/', views.topic, name='topic'),
]