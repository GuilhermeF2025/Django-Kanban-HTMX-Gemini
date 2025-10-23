from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .models import Coluna, Cartao
from .forms import CartaoForm, RegistroForm, ColunaForm

def registrar(request):
    if request.user.is_authenticated: return redirect('quadro_kanban')
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('quadro_kanban')
    else: form = RegistroForm()
    return render(request, 'quadro/registrar.html', {'form': form})

@login_required
def quadro_kanban(request):
    colunas = Coluna.objects.filter(user=request.user).prefetch_related('cartoes')
    contexto = { 'colunas': colunas, 'form': CartaoForm(), 'coluna_form': ColunaForm() }
    return render(request, 'quadro/quadro_kanban.html', contexto)

@login_required
@require_POST
def mover_cartao(request):
    try:
        ordem_cartoes_ids = request.POST.getlist('cartao_ordem')
        coluna_id = request.POST.get('colunaId')
        if not coluna_id: return HttpResponse("ID da coluna não foi encontrado na requisição.", status=400)
        coluna_destino = get_object_or_404(Coluna, id=coluna_id, user=request.user)
        for index, cartao_id in enumerate(ordem_cartoes_ids):
            Cartao.objects.filter(id=cartao_id, user=request.user).update(coluna=coluna_destino, ordem=index)
        return HttpResponse(status=204)
    except Coluna.DoesNotExist: return HttpResponse("Coluna de destino não encontrada no banco de dados.", status=404)
    except Exception as e: return HttpResponse(str(e), status=500)

@login_required
def adicionar_cartao(request, coluna_id):
    coluna = get_object_or_404(Coluna, id=coluna_id, user=request.user)
    if request.method == "POST":
        form = CartaoForm(request.POST)
        if form.is_valid():
            cartao = form.save(commit=False)
            cartao.coluna = coluna
            cartao.user = request.user
            maior_ordem = Cartao.objects.filter(coluna=coluna).order_by('-ordem').first()
            cartao.ordem = (maior_ordem.ordem + 1) if maior_ordem else 0
            cartao.save()
            contexto = {'cartao': cartao, 'coluna': coluna}
            return render(request, 'quadro/_novo_cartao_e_botao.html', contexto)
    else: form = CartaoForm()
    return render(request, 'quadro/_cartao_form.html', {'form': form, 'coluna': coluna})

@login_required
def editar_cartao(request, cartao_id):
    cartao = get_object_or_404(Cartao, id=cartao_id, user=request.user)
    if request.method == 'POST':
        form = CartaoForm(request.POST, instance=cartao)
        if form.is_valid():
            form.save()
            return render(request, 'quadro/_cartao.html', {'cartao': cartao})
    else: form = CartaoForm(instance=cartao)
    return render(request, 'quadro/_cartao_edit_form.html', {'form': form, 'cartao': cartao})

@login_required
def get_cartao(request, cartao_id):
    cartao = get_object_or_404(Cartao, id=cartao_id, user=request.user)
    return render(request, 'quadro/_cartao.html', {'cartao': cartao})

@login_required
@require_http_methods(["DELETE"])
def excluir_cartao(request, cartao_id):
    cartao = get_object_or_404(Cartao, id=cartao_id, user=request.user)
    cartao.delete()
    return HttpResponse(status=200)

@login_required
@require_POST
def adicionar_coluna(request):
    form = ColunaForm(request.POST)
    if form.is_valid():
        coluna = form.save(commit=False)
        coluna.user = request.user
        maior_ordem = Coluna.objects.filter(user=request.user).order_by('-ordem').first()
        coluna.ordem = (maior_ordem.ordem + 1) if maior_ordem else 0
        coluna.save()
        contexto = { 'coluna': coluna }
        return render(request, 'quadro/_coluna.html', contexto)
    return HttpResponse("Formulário inválido.", status=400)

@login_required
@require_POST
def logout_view(request):
    logout(request)
    response = HttpResponse(status=204) # 204 No Content
    response['HX-Refresh'] = 'true' # Header especial para o HTMX
    return response