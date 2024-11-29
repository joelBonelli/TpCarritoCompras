from django.contrib import messages
from django.forms import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from .models import ProductoBase, ProductoElectronico, ProductoRopa, Carrito, CarritoProductos
from django.contrib.auth import login, authenticate
from .forms import RegistroForm, LoginForm
from django.contrib.contenttypes.models import ContentType

def lista_productos(request):
    productos_electronicos = ProductoElectronico.objects.all()
    productos_ropa = ProductoRopa.objects.all()
    productos = list(productos_electronicos) + list(productos_ropa)
    return render(request, 'mi_app/lista_productos.html', {'productos': productos})

def producto_detalle(request, producto_id):
    producto = get_object_or_404(ProductoElectronico, id=producto_id)
    return render(request, 'mi_app/producto_detalle.html', {'producto': producto})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('lista_productos')  
            else:
                form.add_error(None, 'Correo electrónico o contraseña incorrectos')
    else:
        form = LoginForm()
    return render(request, 'mi_app/login.html', {'form': form})

def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = RegistroForm()
    return render(request, 'mi_app/registro.html', {'form': form})

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(ProductoElectronico, id=producto_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    
    try:
        carrito.agregar_producto(producto)
    except ValidationError:
        return redirect('producto_detalle', producto_id=producto.id)

    return redirect('ver_carrito')

@login_required
def ver_carrito(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    productos_en_carrito = CarritoProductos.objects.filter(carrito=carrito)
    return render(request, 'mi_app/ver_carrito.html', {'carrito': carrito, 'productos_en_carrito': productos_en_carrito})

@login_required
def eliminar_del_carrito(request, producto_id):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    producto = get_object_or_404(ProductoElectronico, id=producto_id)
    carrito.eliminar_producto(producto)
    return redirect('ver_carrito')

@require_POST
def logout_view(request):
    logout(request)
    return redirect('lista_productos')

@login_required
@require_POST
def actualizar_cantidad(request, item_id):
    item_carrito = get_object_or_404(CarritoProductos, id=item_id, carrito__usuario=request.user)
    nueva_cantidad = int(request.POST.get('cantidad', 1))
    
    if nueva_cantidad > item_carrito.producto.stock:
        messages.warning(request, 'La cantidad solicitada excede el stock disponible.')
        return redirect('ver_carrito')

    item_carrito.cantidad = nueva_cantidad
    item_carrito.save()
    return redirect('ver_carrito')

@login_required
def gracias(request):
    carrito = Carrito.objects.filter(usuario=request.user)
    for item in carrito:
        producto = item.producto
        producto.stock -= item.cantidad
        producto.save()
    carrito.delete()
    return render(request, 'mi_app/gracias.html', {'usuario': request.user})


@login_required
def vaciar_carrito(request):
    carrito = Carrito.objects.filter(usuario=request.user)
    carrito.delete()
    return redirect('ver_carrito')