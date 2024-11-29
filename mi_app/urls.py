from django.urls import path
from . import views


urlpatterns = [
        path('', views.lista_productos, name='lista_productos'),
        path('producto/<int:producto_id>/', views.producto_detalle, name='producto_detalle'),
        path('login/', views.login_view, name='login'),
        path('registro/', views.registro_view, name='registro'),
        path('carrito/', views.ver_carrito, name='ver_carrito'),
        path('logout/', views.logout_view, name='logout'),
        path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
        path('eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
        path('actualizar_cantidad/<int:item_id>/', views.actualizar_cantidad, name='actualizar_cantidad'),
        path('gracias/', views.gracias, name='gracias'),
        path('vaciar_carrito/', views.vaciar_carrito, name='vaciar_carrito'),
]