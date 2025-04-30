# Importa as configurações do projeto
from django.conf import settings
# Arquivos estáticos ou de mídia durante o desenvolvimento
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
]

# Ver arquivos de media enviados pelo usuário
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )