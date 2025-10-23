# quadro/admin.py
from django.contrib import admin
from .models import Coluna, Cartao

admin.site.register(Coluna)
admin.site.register(Cartao)