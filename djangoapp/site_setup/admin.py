from django.contrib import admin
from site_setup.models import MenuLink, SiteSetup

# Register your models here.
@admin.register(MenuLink)
class MenuLinkAdmin(admin.ModelAdmin):
    list_display = 'id', 'text', 'url_or_path',
    list_display_links = 'id', 'text', 'url_or_path',
    search_fields = 'id', 'text', 'url_or_path',

@admin.register(SiteSetup)
class SiteSetupAdmin(admin.ModelAdmin):
    list_display = 'title', 'description',

    # Permissão de adicionar novos valores na area administrativa -> No caso, não tera permissão se já tiver algum valor
    def has_add_permission(self, request):
        return not SiteSetup.objects.all()[:1].exists()