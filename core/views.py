#from pyexpat.errors import messages
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ContatoForm, ProdutoModelForm
from core.models import Produto

def index(request):

    produtos = Produto.objects.all()
    context = {
        'produtos': produtos  # Passando a lista de produtos para o template
    }
    return render(request, 'index.html', context)

def contato(request):
    form = ContatoForm(request.POST or None)

    if str(request.method) == 'POST':
        if form.is_valid():
            form.send_mail()
            messages.success(request, 'E-mail enviado com sucesso')
            form = ContatoForm()

        else:
            messages.error(request, 'Erro ao enviar mensagem')

    context = {
        'form': form
}
    return render(request, 'contato.html', context)

def produto(request):
    if str(request.user) != 'AnonymousUser':
        if str(request.method) == 'POST':
            form = ProdutoModelForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Produto salvo com sucesso')
                form = ProdutoModelForm()
            else:
                messages.error(request, 'Erro ao salvar o produto')
        else:
            form = ProdutoModelForm()
        context = {
            'form': form
        }
        return render(request, 'produto.html', context)
    else:
        return redirect('index')

