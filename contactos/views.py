from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .models import Contacto
from .forms import ContactoForm, RegistroForm
from django.contrib.auth.decorators import login_required


@login_required
def inicio(request):
    contactos = Contacto.objects.all()

    return render(request, 'contactos/inicio.html', {
        'contactos': contactos
    })

@login_required
def inicio(request):
    contactos = Contacto.objects.filter(usuario=request.user)

    return render(request, 'contactos/inicio.html', {
        'contactos': contactos
    })

@login_required
def anadir_contacto(request):
    if request.method == 'POST':
        formulario = ContactoForm(request.POST)

        if formulario.is_valid():
            contacto = formulario.save(commit=False)
            contacto.usuario = request.user
            contacto.save()

            return redirect('inicio')
    else:
        formulario = ContactoForm()

    return render(request, 'contactos/anadir_contacto.html', {
        'formulario': formulario
    })

@login_required
def detalle_contacto(request, id):
    contacto = get_object_or_404(
        Contacto,
        id=id,
        usuario=request.user
    )

    return render(request, 'contactos/detalle_contacto.html', {
        'contacto': contacto
    })

@login_required
def editar_contacto(request, id):
    contacto = get_object_or_404(
        Contacto,
        id=id,
        usuario=request.user
    )

    if request.method == 'POST':
        formulario = ContactoForm(request.POST, instance=contacto)

        if formulario.is_valid():
            formulario.save()
            return redirect('detalle_contacto', id=contacto.id)
    else:
        formulario = ContactoForm(instance=contacto)

    return render(request, 'contactos/editar_contacto.html', {
        'formulario': formulario,
        'contacto': contacto
    })

@login_required
def eliminar_contacto(request, id):
    contacto = get_object_or_404(
        Contacto,
        id=id,
        usuario=request.user
    )

    if request.method == 'POST':
        contacto.delete()
        return redirect('inicio')

    return render(request, 'contactos/eliminar_contacto.html', {
        'contacto': contacto
    })

def registro(request):
    if request.method == 'POST':
        formulario = RegistroForm(request.POST)

        if formulario.is_valid():
            formulario.save()
            return redirect('login')
    else:
        formulario = RegistroForm()

    return render(request, 'contactos/registro.html', {
        'formulario': formulario
    })