from django.urls import path
from . import views

urlpatterns = [
    path('', views.quadro_kanban, name='quadro_kanban'),
    path('mover-cartao/', views.mover_cartao, name='mover_cartao'),
    path('coluna/<int:coluna_id>/adicionar-cartao/', views.adicionar_cartao, name='adicionar_cartao'),
    path('cartao/<int:cartao_id>/editar/', views.editar_cartao, name='editar_cartao'),
    path('cartao/<int:cartao_id>/', views.get_cartao, name='get_cartao'),
    path('cartao/<int:cartao_id>/excluir/', views.excluir_cartao, name='excluir_cartao'),
    path('registrar/', views.registrar, name='registrar'),
    path('adicionar-coluna/', views.adicionar_coluna, name='adicionar_coluna'),
    
    # NOVA URL PARA O LOGOUT CUSTOMIZADO
    path('logout/', views.logout_view, name='logout_customizado'),
]