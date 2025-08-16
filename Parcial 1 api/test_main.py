import pytest
from fastapi.testclient import TestClient
from main import app, Producto, Categoria, ProductoCreate

client = TestClient(app)

# Datos de prueba
categoria_valida = {
    "nombre": "Frutas",
    "descripcion": "Productos frutales frescos"
}

producto_valido = {
    "nombre": "Manzana Roja",
    "precio": 25.50,
    "categorias": [categoria_valida],
    "stock": 100
}

class TestModelosPydantic:
    """Pruebas para los modelos Pydantic"""
    
    def test_categoria_valida(self):
        """Prueba que una categoría válida se crea correctamente"""
        categoria = Categoria(**categoria_valida)
        assert categoria.nombre == "Frutas"
        assert categoria.descripcion == "Productos frutales frescos"
    
    def test_categoria_nombre_vacio(self):
        """Prueba que no se puede crear una categoría con nombre vacío"""
        with pytest.raises(ValueError, match="no puede estar vacío"):
            Categoria(nombre="", descripcion="test")
    
    def test_categoria_nombre_muy_largo(self):
        """Prueba que no se puede crear una categoría con nombre muy largo"""
        with pytest.raises(ValueError):
            Categoria(nombre="a" * 51, descripcion="test")
    
    def test_producto_valido(self):
        """Prueba que un producto válido se crea correctamente"""
        producto = ProductoCreate(**producto_valido)
        assert producto.nombre == "Manzana Roja"
        assert producto.precio == 25.50
        assert len(producto.categorias) == 1
        assert producto.stock == 100
    
    def test_producto_precio_negativo(self):
        """Prueba que no se puede crear un producto con precio negativo"""
        datos_invalidos = producto_valido.copy()
        datos_invalidos["precio"] = -10
        with pytest.raises(ValueError, match="debe ser mayor a 0"):
            ProductoCreate(**datos_invalidos)
    
    def test_producto_precio_muy_alto(self):
        """Prueba que no se puede crear un producto con precio muy alto"""
        datos_invalidos = producto_valido.copy()
        datos_invalidos["precio"] = 15000
        with pytest.raises(ValueError, match="no puede exceder"):
            ProductoCreate(**datos_invalidos)
    
    def test_producto_stock_negativo(self):
        """Prueba que no se puede crear un producto con stock negativo"""
        datos_invalidos = producto_valido.copy()
        datos_invalidos["stock"] = -5
        with pytest.raises(ValueError, match="no puede ser negativo"):
            ProductoCreate(**datos_invalidos)
    
    def test_producto_sin_categorias(self):
        """Prueba que no se puede crear un producto sin categorías"""
        datos_invalidos = producto_valido.copy()
        datos_invalidos["categorias"] = []
        with pytest.raises(ValueError, match="debe tener al menos una categoría"):
            ProductoCreate(**datos_invalidos)
    
    def test_producto_categorias_duplicadas(self):
        """Prueba que no se puede crear un producto con categorías duplicadas"""
        datos_invalidos = producto_valido.copy()
        datos_invalidos["categorias"] = [
            {"nombre": "Frutas", "descripcion": "test1"},
            {"nombre": "Frutas", "descripcion": "test2"}
        ]
        with pytest.raises(ValueError, match="categorías duplicadas"):
            ProductoCreate(**datos_invalidos)
    
    def test_producto_demasiadas_categorias(self):
        """Prueba que no se puede crear un producto con demasiadas categorías"""
        datos_invalidos = producto_valido.copy()
        datos_invalidos["categorias"] = [
            {"nombre": f"Categoria{i}", "descripcion": f"test{i}"}
            for i in range(11)
        ]
        with pytest.raises(ValueError, match="más de 10 categorías"):
            ProductoCreate(**datos_invalidos)

class TestEndpoints:
    """Pruebas para los endpoints de la API"""
    
    def test_root_endpoint(self):
        """Prueba el endpoint raíz"""
        response = client.get("/")
        assert response.status_code == 200
        assert "API de Cooperativa" in response.json()["message"]
    
    def test_crear_producto_exitoso(self):
        """Prueba crear un producto exitosamente"""
        response = client.post("/productos/", json=producto_valido)
        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == "Manzana Roja"
        assert data["precio"] == 25.50
        assert data["id"] is not None
        assert data["fecha_creacion"] is not None
    
    def test_crear_producto_datos_invalidos(self):
        """Prueba crear un producto con datos inválidos"""
        datos_invalidos = producto_valido.copy()
        datos_invalidos["precio"] = -10
        response = client.post("/productos/", json=datos_invalidos)
        assert response.status_code == 422
    
    def test_obtener_productos_vacio(self):
        """Prueba obtener productos cuando no hay ninguno"""
        response = client.get("/productos/")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_obtener_productos_con_datos(self):
        """Prueba obtener productos cuando hay datos"""
        # Crear un producto primero
        client.post("/productos/", json=producto_valido)
        
        response = client.get("/productos/")
        assert response.status_code == 200
        productos = response.json()
        assert len(productos) > 0
        assert productos[0]["nombre"] == "Manzana Roja"
    
    def test_obtener_producto_por_id_exitoso(self):
        """Prueba obtener un producto por ID exitosamente"""
        # Crear un producto primero
        create_response = client.post("/productos/", json=producto_valido)
        producto_id = create_response.json()["id"]
        
        response = client.get(f"/productos/{producto_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == producto_id
        assert data["nombre"] == "Manzana Roja"
    
    def test_obtener_producto_por_id_no_existe(self):
        """Prueba obtener un producto por ID que no existe"""
        response = client.get("/productos/123456")
        assert response.status_code == 404
        assert "no encontrado" in response.json()["detail"]
    
    def test_actualizar_producto_exitoso(self):
        """Prueba actualizar un producto exitosamente"""
        # Crear un producto primero
        create_response = client.post("/productos/", json=producto_valido)
        producto_id = create_response.json()["id"]
        
        # Datos actualizados
        datos_actualizados = producto_valido.copy()
        datos_actualizados["nombre"] = "Manzana Verde"
        datos_actualizados["precio"] = 30.00
        
        response = client.put(f"/productos/{producto_id}", json=datos_actualizados)
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "Manzana Verde"
        assert data["precio"] == 30.00
        assert data["id"] == producto_id
    
    def test_actualizar_producto_no_existe(self):
        """Prueba actualizar un producto que no existe"""
        response = client.put("/productos/123456", json=producto_valido)
        assert response.status_code == 404
    
    def test_eliminar_producto_exitoso(self):
        """Prueba eliminar un producto exitosamente"""
        # Crear un producto primero
        create_response = client.post("/productos/", json=producto_valido)
        producto_id = create_response.json()["id"]
        
        response = client.delete(f"/productos/{producto_id}")
        assert response.status_code == 200
        assert "eliminado" in response.json()["message"]
        
        # Verificar que ya no existe
        get_response = client.get(f"/productos/{producto_id}")
        assert get_response.status_code == 404
    
    def test_eliminar_producto_no_existe(self):
        """Prueba eliminar un producto que no existe"""
        response = client.delete("/productos/123456")
        assert response.status_code == 404
    
    def test_obtener_productos_por_categoria(self):
        """Prueba obtener productos filtrados por categoría"""
        # Crear productos con diferentes categorías
        producto1 = {
            "nombre": "Manzana",
            "precio": 25.50,
            "categorias": [{"nombre": "Frutas", "descripcion": "test"}],
            "stock": 100
        }
        producto2 = {
            "nombre": "Zanahoria",
            "precio": 15.00,
            "categorias": [{"nombre": "Verduras", "descripcion": "test"}],
            "stock": 50
        }
        
        client.post("/productos/", json=producto1)
        client.post("/productos/", json=producto2)
        
        response = client.get("/productos/categoria/Frutas")
        assert response.status_code == 200
        productos = response.json()
        assert len(productos) > 0
        assert all("Frutas" in [cat["nombre"] for cat in p["categorias"]] for p in productos)

class TestValidacionesIntegradas:
    """Pruebas específicas para validaciones integradas"""
    
    def test_validacion_nombre_producto_espacios(self):
        """Prueba que los espacios en blanco se manejan correctamente"""
        datos = producto_valido.copy()
        datos["nombre"] = "   Manzana Roja   "
        
        response = client.post("/productos/", json=datos)
        assert response.status_code == 201
        assert response.json()["nombre"] == "Manzana Roja"
    
    def test_validacion_precio_redondeo(self):
        """Prueba que los precios se redondean correctamente"""
        datos = producto_valido.copy()
        datos["precio"] = 25.567
        
        response = client.post("/productos/", json=datos)
        assert response.status_code == 201
        assert response.json()["precio"] == 25.57
    
    def test_validacion_categoria_nombre_formato(self):
        """Prueba que los nombres de categorías se formatean correctamente"""
        datos = producto_valido.copy()
        datos["categorias"] = [{"nombre": "frutas frescas", "descripcion": "test"}]
        
        response = client.post("/productos/", json=datos)
        assert response.status_code == 201
        assert response.json()["categorias"][0]["nombre"] == "Frutas Frescas"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
