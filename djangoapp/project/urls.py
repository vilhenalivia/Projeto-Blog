# Importa as configurações do projeto
from django.conf import settings
# Arquivos estáticos ou de mídia durante o desenvolvimento
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('blog.urls')),
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls'))
]

# Ver arquivos de media enviados pelo usuário
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )