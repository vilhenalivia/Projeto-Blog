from site_setup.models import SiteSetup

def context_processor_example(request):
    return {
        'example': 'Veio do context processor'
    }


def site_setup(request):
    # QUERY -> Consulta na base de dados
    setup = SiteSetup.objects.order_by('-id').first()
    return {
        'site_setup': setup,
    }