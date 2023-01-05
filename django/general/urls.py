from django.urls import path
from django.views.generic import TemplateView

app_name = 'general'
urlpatterns = [
    path('', TemplateView.as_view(template_name="general/coming-soon.html"), name='comingsoon'),
    path('cookies/', TemplateView.as_view(template_name="general/cookies.html"), name='cookies'),
]
