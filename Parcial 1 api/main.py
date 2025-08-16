from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, validator
from typing import List, Optional
import uuid
from datetime import datetime

# Crear la aplicación FastAPI
app = FastAPI(
    title="API Cooperativa de Agricultores",
    description="API interna para registrar productos agrícolas",
    version="1.0.0"
)

# Modelo Pydantic para las categorías
class Categoria(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=50, description="Nombre de la categoría")
    descripcion: Optional[str] = Field(None, max_length=200, description="Descripción opcional de la categoría")
    
    @validator('nombre')
    def validar_nombre_categoria(cls, v):
        if not v.strip():
            raise ValueError('El nombre de la categoría no puede estar vacío')
        return v.strip().title()

# Modelo Pydantic para los productos
class Producto(BaseModel):
    id: Optional[str] = None
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del producto")
    precio: float = Field(..., gt=0, le=10000, description="Precio del producto en pesos")
    categorias: List[Categoria] = Field(..., min_items=1, max_items=10, description="Lista de categorías del producto")
    stock: int = Field(..., ge=0, le=10000, description="Cantidad disponible en stock")
    fecha_creacion: Optional[datetime] = None
    
    @validator('nombre')
    def validar_nombre_producto(cls, v):
        if not v.strip():
            raise ValueError('El nombre del producto no puede estar vacío')
        return v.strip().title()
    
    @validator('precio')
    def validar_precio(cls, v):
        if v <= 0:
            raise ValueError('El precio debe ser mayor a 0')
        if v > 10000:
            raise ValueError('El precio no puede exceder $10,000')
        return round(v, 2)
    
    @validator('stock')
    def validar_stock(cls, v):
        if v < 0:
            raise ValueError('El stock no puede ser negativo')
        if v > 10000:
            raise ValueError('El stock no puede exceder 10,000 unidades')
        return v
    
    @validator('categorias')
    def validar_categorias(cls, v):
        if not v:
            raise ValueError('El producto debe tener al menos una categoría')
        if len(v) > 10:
            raise ValueError('El producto no puede tener más de 10 categorías')
        
        # Validar que no haya categorías duplicadas
        nombres = [cat.nombre.lower() for cat in v]
        if len(nombres) != len(set(nombres)):
            raise ValueError('No puede haber categorías duplicadas')
        
        return v

# Modelo para crear productos (sin ID)
class ProductoCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del producto")
    precio: float = Field(..., gt=0, le=10000, description="Precio del producto en pesos")
    categorias: List[Categoria] = Field(..., min_items=1, max_items=10, description="Lista de categorías del producto")
    stock: int = Field(..., ge=0, le=10000, description="Cantidad disponible en stock")

# Base de datos simulada
productos_db = {}

@app.get("/")
async def root():
    return {"message": "API de Cooperativa de Agricultores - Bienvenido"}

@app.post("/productos/", response_model=Producto, status_code=status.HTTP_201_CREATED)
async def crear_producto(producto: ProductoCreate):
    """
    Crear un nuevo producto con validación integrada.
    
    - **nombre**: Nombre del producto (1-100 caracteres)
    - **precio**: Precio en pesos (mayor a 0, máximo $10,000)
    - **categorias**: Lista de categorías (mínimo 1, máximo 10)
    - **stock**: Cantidad disponible (0-10,000 unidades)
    """
    # Generar ID único
    producto_id = str(uuid.uuid4())
    
    # Crear producto completo
    producto_completo = Producto(
        id=producto_id,
        nombre=producto.nombre,
        precio=producto.precio,
        categorias=producto.categorias,
        stock=producto.stock,
        fecha_creacion=datetime.now()
    )
    
    # Guardar en base de datos simulada
    productos_db[producto_id] = producto_completo
    
    return producto_completo

@app.get("/productos/", response_model=List[Producto])
async def obtener_productos():
    """
    Obtener todos los productos registrados.
    """
    return list(productos_db.values())

@app.get("/productos/{producto_id}", response_model=Producto)
async def obtener_producto(producto_id: str):
    """
    Obtener un producto específico por su ID.
    """
    if producto_id not in productos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    return productos_db[producto_id]

@app.put("/productos/{producto_id}", response_model=Producto)
async def actualizar_producto(producto_id: str, producto: ProductoCreate):
    """
    Actualizar un producto existente con validación integrada.
    """
    if producto_id not in productos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    
    # Crear producto actualizado
    producto_actualizado = Producto(
        id=producto_id,
        nombre=producto.nombre,
        precio=producto.precio,
        categorias=producto.categorias,
        stock=producto.stock,
        fecha_creacion=productos_db[producto_id].fecha_creacion
    )
    
    productos_db[producto_id] = producto_actualizado
    return producto_actualizado

@app.delete("/productos/{producto_id}")
async def eliminar_producto(producto_id: str):
    """
    Eliminar un producto por su ID.
    """
    if producto_id not in productos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    
    del productos_db[producto_id]
    return {"message": "Producto eliminado exitosamente"}

@app.get("/productos/categoria/{nombre_categoria}", response_model=List[Producto])
async def obtener_productos_por_categoria(nombre_categoria: str):
    """
    Obtener productos filtrados por categoría.
    """
    productos_filtrados = []
    for producto in productos_db.values():
        for categoria in producto.categorias:
            if categoria.nombre.lower() == nombre_categoria.lower():
                productos_filtrados.append(producto)
                break
    
    return productos_filtrados

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
