# Plan de trabajo: datos eléctricos del BEN de Paraguay

## Objetivo

Preparar un repositorio versionable en GitHub con una base consultable y trazable de los datos eléctricos extraídos y analizados de las ediciones del Balance Energético Nacional (BEN).

## Alcance inicial

- Ediciones cubiertas por la extracción original: BEN 2020 a BEN 2025.
- La planilla de extracción contiene 107 renglones numéricos de cuadros comparativos, incluidos rótulos originales, valores publicados, variaciones, fuente, localizador y notas.
- El análisis consolidado contiene 60 observaciones de balance de BEN 2021 a BEN 2025, 38 comparaciones interanuales, 24 registros de auditoría de revisiones, 6 niveles de serie histórica y 5 indicadores adicionales de BEN 2025.
- Los datos regulatorios del artículo se documentarán por separado de las observaciones del BEN.
- Los PDF fuente se referenciarán mediante enlaces oficiales; el repositorio conservará la planilla fuente y los CSV exportados.

## Asignación

| Responsable | Tarea | Estado |
| --- | --- | --- |
| Agente 1: inventario BEN | Identificar ediciones, tablas, campos, recuentos y límites de comparabilidad en los archivos fuente | Completado |
| Agente 2: acceso a GitHub | Revisar repositorio local, herramientas y requisitos de publicación sin exponer credenciales | Completado; falta conectar GitHub y definir destino/visibilidad |
| Agente 3: arquitectura | Recomendar estructura de datos, tablas canónicas, resultados derivados y flujo de actualización | Completado |
| Agente coordinador | Integrar la extracción, crear esquema SQLite y generador, documentar consultas y preparar el repositorio local | Completado en local; publicación pendiente de conectar GitHub y definir destino |

## Entregables

1. CSV de los cuadros comparativos publicados, conservando rótulos, signos y notas de origen.
2. CSV de observaciones por edición y año de referencia, con código, unidad y localizador.
3. CSV de resultados derivados del análisis, identificados como tales.
4. Esquema SQL y script Python de biblioteca estándar para reconstruir la base SQLite.
5. README en español con cobertura, procedencia, limitaciones y consultas de ejemplo.
6. Repositorio Git local listo para publicar en GitHub.

## Criterios de aceptación

- BEN 2020–2025 queda representado en las tablas de extracción original.
- Se distinguen edición de publicación y año de referencia; los datos de distintas ediciones no se empalman silenciosamente.
- Los valores publicados mantienen su signo y precisión de origen; los niveles normalizados y cálculos derivados quedan separados.
- Cada fila conserva la procedencia y el localizador disponibles.
- La base SQLite se genera desde los CSV del repositorio y la estructura queda documentada para consulta.
- El alcance y las advertencias de comparabilidad del material original quedan visibles.

## Secuencia

1. Copiar los insumos de BEN y la extracción fuente al nuevo repositorio. **Completado.**
2. Exportar la tabla principal de la planilla a CSV y ordenar los CSV del análisis por función. **Completado.**
3. Crear el esquema SQL y el generador de SQLite. **Completado.**
4. Documentar las tablas, ejemplos de consulta y pasos para actualizar una edición. **Completado.**
5. Preparar el repositorio Git local. **Completado.**
6. Publicar el contenido en Br1Sanabria/ben-electricity-paraguay y verificar que los archivos de datos estén disponibles. **En curso.**

## Decisión de publicación

El repositorio de destino es Br1Sanabria/ben-electricity-paraguay, público, creado por el propietario. La carga de los archivos está en curso.
