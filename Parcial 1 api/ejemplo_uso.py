#!/usr/bin/env python3
"""
Ejemplo de uso de la API de Cooperativa de Agricultores
Demuestra cómo usar todos los endpoints y validaciones
"""

import requests
import json
from typing import Dict, Any

# Configuración
BASE_URL = "http://localhost:8000"

def print_response(response: requests.Response, title: str = ""):
    """Imprime la respuesta de manera formateada"""
    print(f"\n{'='*50}")
    if title:
        print(f"📋 {title}")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print('='*50)

def test_crear_productos():
    """Prueba crear productos válidos e inválidos"""
    print("\n🚀 PROBANDO CREACIÓN DE PRODUCTOS")
    
    # Producto válido
    producto_valido = {
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
    
    response = requests.post(f"{BASE_URL}/productos/", json=producto_valido)
    print_response(response, "✅ Producto Válido Creado")
    
    # Producto con múltiples categorías
    producto_multiple_categorias = {
        "nombre": "Tomate Cherry Orgánico",
        "precio": 45.75,
        "categorias": [
            {
                "nombre": "Verduras",
                "descripcion": "Hortalizas frescas"
            },
            {
                "nombre": "Orgánico",
                "descripcion": "Productos orgánicos certificados"
            },
            {
                "nombre": "Premium",
                "descripcion": "Productos de alta calidad"
            }
        ],
        "stock": 50
    }
    
    response = requests.post(f"{BASE_URL}/productos/", json=producto_multiple_categorias)
    print_response(response, "✅ Producto con Múltiples Categorías")
    
    # Producto con formateo automático
    producto_formateo = {
        "nombre": "   zanahoria naranja   ",
        "precio": 15.99,
        "categorias": [
            {
                "nombre": "   verduras frescas   ",
                "descripcion": "   productos de la huerta   "
            }
        ],
        "stock": 75
    }
    
    response = requests.post(f"{BASE_URL}/productos/", json=producto_formateo)
    print_response(response, "✅ Producto con Formateo Automático")

def test_validaciones():
    """Prueba las validaciones de datos inválidos"""
    print("\n⚠️ PROBANDO VALIDACIONES")
    
    # Precio negativo
    producto_precio_negativo = {
        "nombre": "Test",
        "precio": -10,
        "categorias": [{"nombre": "Test"}],
        "stock": 10
    }
    
    response = requests.post(f"{BASE_URL}/productos/", json=producto_precio_negativo)
    print_response(response, "❌ Precio Negativo")
    
    # Precio muy alto
    producto_precio_alto = {
        "nombre": "Test",
        "precio": 15000,
        "categorias": [{"nombre": "Test"}],
        "stock": 10
    }
    
    response = requests.post(f"{BASE_URL}/productos/", json=producto_precio_alto)
    print_response(response, "❌ Precio Muy Alto")
    
    # Stock negativo
    producto_stock_negativo = {
        "nombre": "Test",
        "precio": 10,
        "categorias": [{"nombre": "Test"}],
        "stock": -5
    }
    
    response = requests.post(f"{BASE_URL}/productos/", json=producto_stock_negativo)
    print_response(response, "❌ Stock Negativo")
    
    # Sin categorías
    producto_sin_categorias = {
        "nombre": "Test",
        "precio": 10,
        "categorias": [],
        "stock": 10
    }
    
    response = requests.post(f"{BASE_URL}/productos/", json=producto_sin_categorias)
    print_response(response, "❌ Sin Categorías")
    
    # Categorías duplicadas
    producto_categorias_duplicadas = {
        "nombre": "Test",
        "precio": 10,
        "categorias": [
            {"nombre": "Frutas", "descripcion": "test1"},
            {"nombre": "Frutas", "descripcion": "test2"}
        ],
        "stock": 10
    }
    
    response = requests.post(f"{BASE_URL}/productos/", json=producto_categorias_duplicadas)
    print_response(response, "❌ Categorías Duplicadas")

def test_operaciones_crud():
    """Prueba las operaciones CRUD"""
    print("\n🔄 PROBANDO OPERACIONES CRUD")
    
    # Crear producto para pruebas
    producto_test = {
        "nombre": "Pera Verde",
        "precio": 30.00,
        "categorias": [{"nombre": "Frutas", "descripcion": "Frutas de temporada"}],
        "stock": 25
    }
    
    response = requests.post(f"{BASE_URL}/productos/", json=producto_test)
    producto_id = response.json()["id"]
    print_response(response, "✅ Producto Creado para CRUD")
    
    # Obtener producto por ID
    response = requests.get(f"{BASE_URL}/productos/{producto_id}")
    print_response(response, "📖 Obtener Producto por ID")
    
    # Actualizar producto
    producto_actualizado = {
        "nombre": "Pera Amarilla",
        "precio": 35.50,
        "categorias": [
            {"nombre": "Frutas", "descripcion": "Frutas de temporada"},
            {"nombre": "Premium", "descripcion": "Productos premium"}
        ],
        "stock": 30
    }
    
    response = requests.put(f"{BASE_URL}/productos/{producto_id}", json=producto_actualizado)
    print_response(response, "✏️ Producto Actualizado")
    
    # Obtener todos los productos
    response = requests.get(f"{BASE_URL}/productos/")
    print_response(response, "📋 Todos los Productos")
    
    # Filtrar por categoría
    response = requests.get(f"{BASE_URL}/productos/categoria/Frutas")
    print_response(response, "🔍 Productos por Categoría 'Frutas'")
    
    # Eliminar producto
    response = requests.delete(f"{BASE_URL}/productos/{producto_id}")
    print_response(response, "🗑️ Producto Eliminado")
    
    # Verificar que ya no existe
    response = requests.get(f"{BASE_URL}/productos/{producto_id}")
    print_response(response, "❌ Producto No Encontrado (después de eliminar)")

def test_casos_especiales():
    """Prueba casos especiales y edge cases"""
    print("\n🎯 PROBANDO CASOS ESPECIALES")
    
    # Producto con precio con muchos decimales
    producto_decimales = {
        "nombre": "Uva Moscatel",
        "precio": 12.56789,
        "categorias": [{"nombre": "Frutas", "descripcion": "Uvas especiales"}],
        "stock": 40
    }
    
    response = requests.post(f"{BASE_URL}/productos/", json=producto_decimales)
    print_response(response, "✅ Precio con Decimales (Redondeado)")
    
    # Producto con stock máximo
    producto_stock_max = {
        "nombre": "Papa Blanca",
        "precio": 8.50,
        "categorias": [{"nombre": "Tubérculos", "descripcion": "Tubérculos frescos"}],
        "stock": 10000
    }
    
    response = requests.post(f"{BASE_URL}/productos/", json=producto_stock_max)
    print_response(response, "✅ Stock Máximo")
    
    # Producto con precio máximo
    producto_precio_max = {
        "nombre": "Azafrán Premium",
        "precio": 10000.00,
        "categorias": [{"nombre": "Especias", "descripcion": "Especias premium"}],
        "stock": 5
    }
    
    response = requests.post(f"{BASE_URL}/productos/", json=producto_precio_max)
    print_response(response, "✅ Precio Máximo")

def main():
    """Función principal que ejecuta todas las pruebas"""
    print("🌾 API COOPERATIVA DE AGRICULTORES - EJEMPLO DE USO")
    print("Asegúrate de que el servidor esté ejecutándose en http://localhost:8000")
    
    try:
        # Probar que el servidor esté funcionando
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Servidor funcionando correctamente")
        else:
            print("❌ Error conectando al servidor")
            return
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor. Asegúrate de que esté ejecutándose.")
        print("Ejecuta: python main.py")
        return
    
    # Ejecutar todas las pruebas
    test_crear_productos()
    test_validaciones()
    test_operaciones_crud()
    test_casos_especiales()
    
    print("\n🎉 ¡Todas las pruebas completadas!")
    print("\n📚 Para más información:")
    print("- Documentación interactiva: http://localhost:8000/docs")
    print("- Documentación ReDoc: http://localhost:8000/redoc")

if __name__ == "__main__":
    main()
