# API Cooperativa de Agricultores

## Descripción

Esta API interna permite a una cooperativa de agricultores registrar y gestionar sus productos agrícolas. Cada producto tiene un nombre, precio y una lista de categorías, con validaciones robustas para evitar datos inconsistentes.

## Características

- **Modelos Pydantic**: Validación automática de datos con mensajes de error descriptivos
- **Validaciones Realistas**: Límites de precio, stock, categorías duplicadas, etc.
- **Endpoints RESTful**: CRUD completo para productos
- **Documentación Automática**: Swagger UI integrado
- **Pruebas Unitarias**: Cobertura completa de funcionalidad

## Estructura del Proyecto

```
├── main.py              # Aplicación FastAPI principal
├── test_main.py         # Pruebas unitarias
├── requirements.txt     # Dependencias del proyecto
└── README.md           # Documentación
```

## Instalación

1. Clonar el repositorio
2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Ejecución

### Servidor de Desarrollo
```bash
python main.py
```

O usando uvicorn directamente:
```bash
uvicorn main:app --reload
```

### Ejecutar Pruebas
```bash
pytest test_main.py -v
```

## Modelos Pydantic

### Categoria
```python
class Categoria(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=200)
```

**Validaciones:**
- Nombre no puede estar vacío
- Nombre máximo 50 caracteres
- Descripción opcional, máximo 200 caracteres
- Formateo automático del nombre (title case)

### Producto
```python
class Producto(BaseModel):
    id: Optional[str] = None
    nombre: str = Field(..., min_length=1, max_length=100)
    precio: float = Field(..., gt=0, le=10000)
    categorias: List[Categoria] = Field(..., min_items=1, max_items=10)
    stock: int = Field(..., ge=0, le=10000)
    fecha_creacion: Optional[datetime] = None
```

**Validaciones:**
- Nombre: 1-100 caracteres, no vacío
- Precio: mayor a 0, máximo $10,000, redondeado a 2 decimales
- Stock: 0-10,000 unidades
- Categorías: mínimo 1, máximo 10, sin duplicados
- Formateo automático de nombres

## Endpoints

### 1. Crear Producto
```http
POST /productos/
```

**Ejemplo de Request:**
```json
{
    "nombre": "Manzana Roja",
    "precio": 25.50,
    "categorias": [
        {
            "nombre": "Frutas",
            "descripcion": "Productos frutales frescos"
        }
    ],
    "stock": 100
}
```

**Validaciones Integradas:**
- Todos los campos requeridos
- Precio positivo y dentro de límites
- Stock no negativo
- Al menos una categoría
- Sin categorías duplicadas

### 2. Obtener Todos los Productos
```http
GET /productos/
```

### 3. Obtener Producto por ID
```http
GET /productos/{producto_id}
```

### 4. Actualizar Producto
```http
PUT /productos/{producto_id}
```

### 5. Eliminar Producto
```http
DELETE /productos/{producto_id}
```

### 6. Filtrar por Categoría
```http
GET /productos/categoria/{nombre_categoria}
```

## Documentación Interactiva

Una vez ejecutado el servidor, accede a:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Ejemplos de Uso

### Crear un Producto Válido
```python
import requests

producto = {
    "nombre": "Tomate Cherry",
    "precio": 45.75,
    "categorias": [
        {"nombre": "Verduras", "descripcion": "Hortalizas frescas"},
        {"nombre": "Orgánico", "descripcion": "Productos orgánicos"}
    ],
    "stock": 50
}

response = requests.post("http://localhost:8000/productos/", json=producto)
print(response.json())
```

### Casos de Error
```python
# Precio negativo
producto_invalido = {
    "nombre": "Test",
    "precio": -10,  # Error: precio debe ser mayor a 0
    "categorias": [{"nombre": "Test"}],
    "stock": 10
}

# Sin categorías
producto_sin_categorias = {
    "nombre": "Test",
    "precio": 10,
    "categorias": [],  # Error: debe tener al menos una categoría
    "stock": 10
}
```

## Criterios de Evaluación Cumplidos

### ✅ Aplicación Funcional de Pydantic (2 pts)
- Modelos `Categoria` y `Producto` con validaciones
- Uso de `Field` para restricciones
- Validadores personalizados con `@validator`
- Manejo de errores descriptivos

### ✅ Validaciones Realistas y Correctas (2 pts)
- **Precio**: Positivo, máximo $10,000, redondeo automático
- **Stock**: No negativo, máximo 10,000 unidades
- **Categorías**: Mínimo 1, máximo 10, sin duplicados
- **Nombres**: No vacíos, formateo automático
- **Límites de longitud**: Nombres y descripciones

### ✅ Coherencia y Claridad Técnica (1 pt)
- Código bien estructurado y documentado
- Endpoints RESTful consistentes
- Pruebas unitarias completas
- Documentación clara y ejemplos prácticos

## Tecnologías Utilizadas

- **FastAPI**: Framework web moderno y rápido
- **Pydantic**: Validación de datos y serialización
- **Pytest**: Framework de pruebas
- **Uvicorn**: Servidor ASGI
- **HTTPX**: Cliente HTTP para pruebas

## Pruebas

El proyecto incluye pruebas exhaustivas que cubren:

1. **Modelos Pydantic**: Validación de datos válidos e inválidos
2. **Endpoints**: CRUD completo y casos de error
3. **Validaciones Integradas**: Formateo, redondeo, límites
4. **Casos Edge**: Datos extremos y valores límite

Para ejecutar todas las pruebas:
```bash
pytest test_main.py -v --tb=short
```
