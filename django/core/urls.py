from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    # General app's urls
    path('', include('general.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
