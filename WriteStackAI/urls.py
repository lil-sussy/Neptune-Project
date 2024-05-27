from django.urls import path
from django.views.generic import TemplateView
from django.urls import include

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html")),
    path('text/', include('text.urls')),
]
