from django.db import models
from django.forms import ValidationError
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class ProductoBase(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(max_length=255, null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.nombre
    
    def ajustar_stock(self, cantidad):
        if self.stock + cantidad < 0:
            raise ValidationError("No hay suficiente stock")
        self.stock += cantidad
        self.save()

class ProductoElectronico(ProductoBase):
    garantia = models.PositiveIntegerField(help_text="Garantía en meses")

class ProductoRopa(ProductoBase):
    talla = models.CharField(max_length=50)
    color = models.CharField(max_length=50)

class Carrito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

    def agregar_producto(self, producto, cantidad=1):
        content_type = ContentType.objects.get_for_model(producto)
        item_carrito, created = CarritoProductos.objects.get_or_create(
            carrito=self, 
            producto_content_type=content_type,
            producto_object_id=producto.id
        )
        if not created:
            item_carrito.cantidad += cantidad
        item_carrito.save()

    def eliminar_producto(self, producto):
        content_type = ContentType.objects.get_for_model(producto)
        item_carrito = CarritoProductos.objects.get(
            carrito=self, 
            producto_content_type=content_type,
            producto_object_id=producto.id
        )
        item_carrito.delete()

class CarritoProductos(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    producto_object_id = models.PositiveIntegerField()
    producto = GenericForeignKey('producto_content_type', 'producto_object_id')
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en {self.carrito}"
    
class UsuarioManager(BaseUserManager):
    def create_user(self, email, nombre, apellido, dni, password=None):
        if not email:
            raise ValueError('El usuario debe tener un email.')
        if not password:
            raise ValueError('El usuario debe tener una contraseña.')
        user = self.model(
            email=self.normalize_email(email),
            nombre=nombre,
            apellido=apellido,
            dni=dni,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nombre, apellido, dni, password=None):
        user = self.create_user(
            email=email,
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser):
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    dni = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'dni']

    def __str__(self):
        return f"{self.nombre} {self.apellido}"