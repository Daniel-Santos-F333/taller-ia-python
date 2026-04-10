# Tests Automatizados para el Backend

Este directorio contiene los scripts automatizados de pruebas para validar el funcionamiento del backend de la aplicación Flask.

## Estructura de Tests

- `conftest.py`: Configuración común para pytest, incluyendo fixtures para la app Flask y limpieza de datos.
- `test_initialization.py`: Pruebas de inicialización de la app y archivos de datos.
- `test_routes_get.py`: Pruebas de rutas GET (páginas).
- `test_forms_post.py`: Pruebas de formularios POST y operaciones CRUD.
- `test_business_flows.py`: Pruebas de flujos de negocio completos.
- `test_errors.py`: Pruebas de manejo de errores y casos límite.
- `test_persistence.py`: Pruebas de persistencia de datos y estabilidad.
- `test_services.py`: Pruebas existentes del sistema.

## Cómo Ejecutar los Tests

1. Asegurarse de que las dependencias estén instaladas:
   ```
   pip install -r requirements.txt
   ```

2. Ejecutar todos los tests:
   ```
   pytest
   ```

3. Ejecutar tests específicos:
   ```
   pytest test_initialization.py
   pytest test_routes_get.py::test_index_page
   ```

4. Ejecutar con verbose:
   ```
   pytest -v
   ```

## Cobertura de Pruebas

Los tests cubren todos los puntos del archivo `backend_manual_tests.md`:

- ✅ Inicialización y rutas GET
- ✅ Formularios y operaciones POST
- ✅ Flujos de negocio completos
- ✅ Manejo de errores y validaciones
- ✅ Persistencia y estabilidad

## Mejoras Implementadas

Durante la creación de los tests, se implementaron las siguientes mejoras en el código:

- **Validación de campos requeridos**: Agregada validación en rutas POST para evitar datos vacíos.
- **Mensajes de error mejorados**: Flash messages para errores de validación.
- **Dependencias actualizadas**: Agregado `requests` y `pytest` a `requirements.txt`.

## Notas

- Los tests usan el Flask test client, por lo que no requieren que el servidor esté corriendo.
- La fixture `clean_data` asegura que los archivos JSON se limpien antes y después de cada test.
- Los tests están diseñados para ser independientes y no afectar datos reales.