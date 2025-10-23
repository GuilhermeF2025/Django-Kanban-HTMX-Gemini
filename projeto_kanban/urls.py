from django.contrib import admin
from django.urls import path, include # Adicione 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    # Adiciona todas as URLs de autenticação do Django (login, logout, reset de senha, etc.)
    # Elas estarão sob o prefixo /contas/ (ex: /contas/login/)
    path('contas/', include('django.contrib.auth.urls')),
    
    # Nossa URL principal do app
    path('', include('quadro.urls')),
]