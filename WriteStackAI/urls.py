from django.urls import path
from django.views.generic import TemplateView
from django.urls import include
# urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html")),
    path('text/', include('text.urls')),
]
# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
