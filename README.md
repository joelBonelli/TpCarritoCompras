Cuando clonen el repositorio tiene que ejecutar: " pip install -r requirements.txt " con ese se instalan todas las dependencias.

### Diagrama de Clases

```mermaid
classDiagram
    %% Clases y Atributos
    class ProductoBase {
        <<abstract>>
        - String nombre
        - String descripcion
        - float precio
        - int stock
        + ajustar_stock()
    }
    
    class ProductoElectronico {
        - int garantia
    }
    
    class ProductoRopa {
        - String talle
        - String color
    }

    class Carrito {
        - Usuario usuario
        - Date fecha_creacion
        - Date actualizado
        + agregar_producto()
        + eliminar_producto()
    }

    class CarritoProducto {
        - Carrito carrito
        - ProductoBase producto
        - int cantidad
        + modificar_cantidad()
    }

    class Usuario {
        - String email
        - String nombre
        - String apellido
        - String dni
        + registrase()
        + seleccionar_producto()
        + comprar()
    }

    %% Relaciones
    ProductoBase <|-- ProductoElectronico
    ProductoBase <|-- ProductoRopa
    Carrito "1" --> "0..*" CarritoProducto : contiene
    CarritoProducto "1" --> "1" ProductoBase : relaciona
    CarritoProducto "1" --> "1" Carrito : pertenece
    Carrito "1" --> "1" Usuario : gestionado_por

```

### Diagrama de Secuencia

```mermaid
sequenceDiagram
    participant Usuario
    participant Carrito
    participant CarritoProducto
    participant ProductoBase

    Usuario->>Carrito: agregar_producto(producto, cantidad)
    Carrito->>ProductoBase: verificar_stock(producto)
    alt stock_disponible
        ProductoBase-->>Carrito: stock_disponible
        Carrito->>CarritoProducto: crear(producto, cantidad)
        CarritoProducto-->>Carrito: producto_agregado
        Carrito-->>Usuario: confirmacion_agregado
    else stock_no_disponible
        ProductoBase-->>Carrito: stock_no_disponible
        Carrito-->>Usuario: error_stock_insuficiente
    end

```

### Diagrama Entidad - Relación


```mermaid
erDiagram
    Usuario {
        email String
        nombre String
        apellido String
        dni String
    }

    Carrito {
        id Integer
        fecha_creacion Date
        actualizado Date
        usuario_id Integer
    }

    ProductoBase {
        id Integer
        nombre String
        descripcion String
        precio Float
        stock Integer
    }

    ProductoElectronico {
        id Integer
        garantia Integer
        producto_base_id Integer
    }

    ProductoRopa {
        id Integer
        talle String
        color String
        producto_base_id Integer
    }

    CarritoProducto {
        id Integer
        cantidad Integer
        carrito_id Integer
        producto_id Integer
    }

    %% Relaciones
    Usuario ||--|| Carrito : posee_uno
    Carrito ||--o{ CarritoProducto : contiene
    ProductoBase ||--o{ CarritoProducto : incluido_en
    ProductoBase ||--o{ ProductoElectronico : especializacion
    ProductoBase ||--o{ ProductoRopa : especializacion

```

### Diccionario de Datos

- **Usuario**
  - email: String - Correo electrónico del usuario.
  - nombre: String - Nombre del usuario.
  - apellido: String - Apellido del usuario.
  - dni: String - Documento Nacional de Identidad del usuario.

- **Carrito**
  - id: Integer - Identificador único del carrito.
  - fecha_creacion: Date - Fecha de creación del carrito.
  - actualizado: Date - Fecha de la última actualización del carrito.
  - usuario_id: Integer - Identificador del usuario que posee el carrito.

- **ProductoBase**
  - id: Integer - Identificador único del producto.
  - nombre: String - Nombre del producto.
  - descripcion: String - Descripción del producto.
  - precio: Float - Precio del producto.
  - stock: Integer - Cantidad de producto disponible en inventario.

- **ProductoElectronico** (hereda de ProductoBase)
  - id: Integer - Identificador único del producto electrónico.
  - garantia: Integer - Duración de la garantía del producto electrónico en meses.
  - producto_base_id: Integer - Identificador del producto base asociado.

- **ProductoRopa** (hereda de ProductoBase)
  - id: Integer - Identificador único del producto de ropa.
  - talle: String - Talla de la prenda.
  - color: String - Color de la prenda.
  - producto_base_id: Integer - Identificador del producto base asociado.

- **CarritoProducto**
  - id: Integer - Identificador único de la relación carrito-producto.
  - cantidad: Integer - Cantidad del producto en el carrito.
  - carrito_id: Integer - Identificador del carrito asociado.
  - producto_id: Integer - Identificador del producto asociado.

### Relaciones

- Un **Usuario** posee uno **Carrito**.
- Un **Carrito** contiene múltiples **CarritoProducto**.
- Un **ProductoBase** está incluido en múltiples **CarritoProducto**.
- **ProductoElectronico** y **ProductoRopa** son especializaciones de **ProductoBase**.

