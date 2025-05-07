# Gerar letras aleatórias 
from random import SystemRandom
import string
from django.utils.text import slugify

def random_letters(k=5):
    return ''.join( SystemRandom().choices(
        string.ascci_letters + string.digits,
        k = k
    ))


def slugify_new(text):
    return slugify(text) + random_letters(4)