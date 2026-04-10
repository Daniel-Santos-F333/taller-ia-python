# Pruebas Manuales para el Programa Completo (Backend)

## Objetivo
Guía completa de pruebas manuales para validar el funcionamiento del backend de la aplicación Flask, incluyendo rutas, servicios, persistencia y manejo de errores. Estas pruebas aseguran que el programa esté pulido y funcional.

## Estructura de pruebas
1. Preparación del entorno
2. Pruebas de inicialización y rutas GET
3. Pruebas de formularios y rutas POST
4. Flujos de negocio completos
5. Pruebas de errores y manejo de excepciones
6. Validación de persistencia y estabilidad

---

## 1. Preparación del entorno

### 1.1 Verificar dependencias
- Ejecutar `pip install -r requirements.txt`
- Confirmar que Flask esté instalado

### 1.2 Iniciar la aplicación
- Ejecutar `python run.py`
- Verificar que el servidor inicie en `http://localhost:5000`
- Confirmar que no hay errores en la consola

### 1.3 Preparar datos de prueba
- Asegurar que los archivos `data/*.json` existan (vacíos o con datos conocidos)
- Opcional: hacer backup de datos existentes

---

## 2. Pruebas de inicialización y rutas GET

### 2.1 Página principal (/)
- Acción: navegar a `http://localhost:5000/`
- Verificar:
  - Se carga la página `index.html`
  - Muestra contadores de computadoras y campers
  - No hay errores 500

### 2.2 Gestión de computadoras (/computers)
- Acción: navegar a `http://localhost:5000/computers`
- Verificar:
  - Se carga la página `computers.html`
  - Muestra lista de computadoras existentes
  - Formulario para agregar nueva computadora visible

### 2.3 Gestión de campers (/campers)
- Acción: navegar a `http://localhost:5000/campers`
- Verificar:
  - Se carga la página `campers.html`
  - Muestra lista de campers existentes
  - Formulario para agregar nuevo camper visible

### 2.4 Historial (/history)
- Acción: navegar a `http://localhost:5000/history`
- Verificar:
  - Se carga la página `history.html`
  - Muestra tabla con historial de asignaciones
  - Datos se muestran correctamente (nombres, fechas, estado)

---

## 3. Pruebas de formularios y rutas POST

### 3.1 Agregar computadora
- Acción: en `/computers`, llenar formulario con datos válidos (serial, brand, model) y enviar
- Verificar:
  - Redirección a `/computers`
  - Nueva computadora aparece en la lista
  - Datos se guardan en `data/computers.json` con ID generado y status "disponible"

### 3.2 Agregar camper
- Acción: en `/campers`, llenar formulario con datos válidos (id, name, email) y enviar
- Verificar:
  - Redirección a `/campers`
  - Nuevo camper aparece en la lista
  - Datos se guardan en `data/campers.json`

### 3.3 Asignar equipo
- Acción: en `/`, seleccionar camper y computadora disponible, enviar formulario de asignación
- Verificar:
  - Mensaje flash de éxito: "Asignación exitosa"
  - Computadora cambia a status "asignado" en la lista
  - Nuevo registro en `data/assignments.json`

### 3.4 Devolver equipo
- Acción: en `/`, hacer clic en "Devolver" para una computadora asignada
- Verificar:
  - Mensaje flash: "Equipo devuelto y puesto en disponibilidad"
  - Computadora vuelve a status "disponible"
  - Asignación se marca con fecha de retorno

---

## 4. Flujos de negocio completos

### 4.1 Flujo completo: registro → asignación → devolución
- Paso 1: agregar computadora y camper
- Paso 2: asignar la computadora al camper
- Paso 3: devolver la computadora
- Verificar:
  - Estado cambia correctamente en cada paso
  - Historial refleja todas las operaciones
  - No hay inconsistencias en los datos JSON

### 4.2 Múltiples asignaciones
- Acción: crear varias computadoras y campers, hacer asignaciones cruzadas
- Verificar:
  - Cada asignación es independiente
  - Computadoras no disponibles no se pueden asignar
  - Historial muestra todas las operaciones correctamente

### 4.3 Consulta de datos después de operaciones
- Acción: después de operaciones, refrescar páginas y verificar que los datos se actualicen
- Verificar:
  - Listas en `/computers` y `/campers` reflejan cambios
  - Dashboard en `/` muestra contadores correctos

---

## 5. Pruebas de errores y manejo de excepciones

### 5.1 Página no encontrada (404)
- Acción: navegar a `http://localhost:5000/ruta-inexistente`
- Verificar:
  - Se muestra página `errors/404.html`
  - Código de estado 404

### 5.2 Error interno (500)
- Acción: simular error (ej. corromper un JSON temporalmente)
- Verificar:
  - Se muestra página `errors/500.html`
  - Código de estado 500
  - Aplicación no se rompe completamente

### 5.3 Asignación de computadora no disponible
- Acción: intentar asignar una computadora ya asignada
- Verificar:
  - Mensaje flash de error: "El computador no está disponible o no existe"
  - No se crea nueva asignación

### 5.4 Datos inválidos en formularios
- Acción: enviar formularios con campos vacíos o datos incorrectos
- Verificar:
  - Aplicación maneja gracefully (no 500)
  - Posiblemente muestra validación o ignora entrada inválida

### 5.5 Archivos JSON corruptos
- Acción: editar manualmente un JSON para que sea inválido
- Verificar:
  - `read_json()` devuelve lista vacía
  - Aplicación continúa funcionando sin crashear

---

## 6. Validación de persistencia y estabilidad

### 6.1 Persistencia de datos
- Acción: reiniciar el servidor y verificar que los datos persisten
- Verificar:
  - Datos en JSON se mantienen entre reinicios
  - Aplicación carga datos correctamente al iniciar

### 6.2 Formato JSON
- Acción: inspeccionar archivos `data/*.json` después de operaciones
- Verificar:
  - JSON válido y bien formateado (indentado)
  - No hay datos duplicados o perdidos

### 6.3 Rendimiento básico
- Acción: realizar múltiples operaciones rápidamente
- Verificar:
  - No hay delays excesivos
  - Aplicación responde consistentemente

---

## Recomendaciones para mejorar la pulidez
- **Validación de entrada**: agregar validaciones en rutas POST para campos requeridos y formatos (ej. email válido).
- **Manejo de excepciones**: envolver operaciones de archivo en try-except más específicos para mejor logging.
- **Mensajes de usuario**: mejorar mensajes flash para casos de error específicos.
- **Automatización**: considerar convertir estas pruebas en scripts o usar herramientas como Postman para testing de API.

---

## Prioridad de ejecución
1. Inicialización y rutas básicas
2. Formularios y operaciones CRUD
3. Flujos completos de negocio
4. Manejo de errores y casos límite
5. Persistencia y estabilidad a largo plazo</content>
<parameter name="filePath">c:\Users\Daniel\Documents\taller-ia-python\backend_manual_tests.md