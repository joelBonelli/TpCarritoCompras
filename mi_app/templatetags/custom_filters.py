from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return value * arg
    except (TypeError, ValueError):
        return 0

@register.filter
def sum_cart_total(productos_en_carrito):
    total = sum(item.producto.precio * item.cantidad for item in productos_en_carrito)
    return total