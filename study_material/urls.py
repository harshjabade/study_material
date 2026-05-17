from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from materials import views as materials_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', materials_views.login_view, name='home_redirect'),
    path('app/', include('materials.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)