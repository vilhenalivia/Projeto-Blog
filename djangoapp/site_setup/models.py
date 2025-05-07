from django.db import models
from utils.model_validators import validate_png
from utils.images import resize_image

# Create your models here.

# MODEL MENU
# Pertence ao SiteSetup
class MenuLink(models.Model):
    class Meta:
        verbose_name ="Menu Link"
        verbose_name_plural = "Menu Links"

    text = models.CharField(max_length=50)
    url_or_path = models.CharField(max_length=2048)
    # Abrir um uma nova área ou não 
    new_tab = models.BooleanField(default=False)
    site_setup = models.ForeignKey(
        'SiteSetup', on_delete=models.CASCADE, blank=True, null=True,
        related_name='menu', default=None,
    )


    def __str__ (self):
        return self.text


# MODEL SITE-SETUP
class SiteSetup(models.Model):
    class Meta: 
        verbose_name = 'Setup'
        verbose_name_plural = 'Setup'

    title = models.CharField(max_length=65)
    description = models.CharField(max_length=255)

    show_header = models.BooleanField(default=True)
    show_search = models.BooleanField(default=True)
    show_menu = models.BooleanField(default=True)
    show_description = models.BooleanField(default=True)
    show_pagination = models.BooleanField(default=True)
    show_footer = models.BooleanField(default=True)

    # Icone para pagina
    favicon = models.ImageField(
        # Caminho da imagem
        upload_to= "assets/favicon/%Y/%m",
        blank=True, default='', validators=[validate_png]
    )

    # Sobrescrita do save para fazer algo antecendente a ele ou após.
    def save(self, *args, **kwargs):
        current_favicon_name = str(self.favicon.name)
        super().save(*args, **kwargs)
        favicon_changed =False

        if self.favicon:
            favicon_changed = current_favicon_name != self.favicon.name
        
        if favicon_changed:
            resize_image(self.favicon, 32)

    def __str__(self):
        return self.title


