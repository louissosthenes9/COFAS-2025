from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include

from cofas_2024 import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('applications.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)