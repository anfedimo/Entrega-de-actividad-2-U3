# Arquitectura NoSQL y Modelado de Documentos: Caso Ecommify

**Maestría en Arquitectura de Software - Universidad de La Sabana**

**Autores:**
* **LUIS ALFREDO GONZALEZ MERCADO**
* **ANDRES FERNANDO DIAZ MORENO**
* **CARLOS ALBERTO AREVALO MARTINEZ**
* **ANDRES CAMILO LOPEZ CASTRO**

**Módulo:** Paradigma NoSQL y Modelado de Documentos

---

## 1. Introducción
Este repositorio contiene la implementación práctica de la Etapa 1 del proyecto Ecommify. El objetivo principal es diseñar una arquitectura de datos orientada a documentos utilizando MongoDB, implementando esquemas flexibles que se adapten a los requisitos técnicos y comerciales de un catálogo de comercio electrónico.

## 2. Estructura del Repositorio
Se ha implementado una arquitectura modular para la ejecución secuencial de la infraestructura de datos:
* `00_ecommify_nosql_architecture.ipynb`: Cuaderno de Google Colab con el flujo completo de ejecución.
* `01_schema_seeder.py`: Script encargado de la conexión a MongoDB Atlas y la inserción masiva (bulk insert) de los 1000 productos bajo el esquema flexible.
* `02_reviews_and_lookup.py`: Script para la generación de la colección externa de reseñas y la validación del modelo relacional mediante la operación de agregación `$lookup`.

## 3. Configuración de la Infraestructura (MongoDB Atlas)
El entorno de base de datos se aprovisionó en **MongoDB Atlas** bajo los siguientes parámetros de arquitectura de red y seguridad:
* **Proveedor Cloud:** AWS (Región `us-east-1`, N. Virginia).
* **Capa (Tier):** M0 Sandbox (Free Tier).
* **Control de Acceso (IAM):** Autenticación mediante usuario administrador de base de datos.
* **Seguridad de Red:** Lista de acceso IP configurada para permitir la conexión del entorno de ejecución dinámico (Google Colab).

*(Nota: Inserta aquí la captura de pantalla de tu conexión exitosa en Colab)*

## 4. Diseño del Esquema de Datos y Patrones Arquitectónicos
Debido a la naturaleza heterogénea del catálogo de productos de Ecommify, se optó por un modelo de "Esquema Flexible" (*Schema-less* controlado). Se implementaron los siguientes patrones de diseño de MongoDB (MongoDB, Inc., 2025):

### 4.1. Esquema Flexible (Polimorfismo)
Se definieron atributos inmutables en la raíz del documento (`_id`, `name`, `category`, `price`) para optimizar índices generales. Las características variables se encapsularon en el subdocumento dinámico `specifications`. Esto evita la proliferación de campos nulos (`null`) en categorías que no comparten los mismos atributos (ej. un procesador de laptop vs. la talla de una camisa).

### 4.2. Computed Pattern (Métricas Precalculadas)
Para soportar cargas de trabajo intensivas en lectura (*read-heavy workloads*), se implementó el bloque `computed_metrics` (conteniendo `total_units_sold` y `average_rating`). Este patrón evita el costo computacional de realizar operaciones de agregación en tiempo real sobre miles de reseñas durante la carga del catálogo.

### 4.3. Extended Reference Pattern (Relaciones)
Las reseñas de los usuarios se modelaron como un arreglo de referencias externas (ObjectIds) en el campo `reviews`. Esta decisión arquitectónica previene el crecimiento descontrolado del documento (*unbounded growth*) en caso de que un producto reciba miles de calificaciones.

*(Nota: Inserta aquí una captura de pantalla del documento JSON de muestra generado en consola)*

## 5. Validación del Modelo (Aggregation Pipelines)
Para comprobar la viabilidad operativa del diseño, se desarrollaron tres *pipelines* de agregación analítica:
1. **Pipeline de Métricas:** Validación del *Computed Pattern* extrayendo el Top 3 de productos más vendidos con latencia mínima, sin realizar conteos en tiempo de ejecución.
2. **Pipeline de Atributos Dinámicos:** Búsqueda polimórfica sobre atributos exclusivos de la categoría ropa (ej. filtrando estrictamente por el campo dinámico `size`).
3. **Pipeline de Referencia Extendida ($lookup):** Demostración técnica de la unión relacional (*JOIN*) entre la colección principal `products` y la colección externa `reviews`, consolidando los comentarios de los usuarios en una sola consulta sin saturar la colección origen.

*(Nota: Inserta aquí las capturas de pantalla de los resultados de tus 3 consultas)*

## 6. Referencias
MongoDB, Inc. (2025). *Data modeling patterns*. MongoDB Manual. Recuperado de https://www.mongodb.com/docs/manual/data-modeling/design-patterns/