# Datos de electricidad del Balance Energético Nacional de Paraguay

Repositorio de datos consultables para el análisis de electricidad del Balance Energético Nacional (BEN). La cobertura inicial reúne cuadros comparativos de las ediciones BEN 2020–BEN 2025 y las tablas consolidadas del análisis eléctrico.

## Cobertura

- **6 ediciones:** BEN 2020 a BEN 2025.
- **107 renglones** exportados de los cuadros comparativos de electricidad de la planilla fuente.
- **60 observaciones** de balance con edición y año de referencia explícitos, tomadas del análisis BEN 2021–BEN 2025.
- **38 comparaciones** interanuales, **24 registros** de revisión entre ediciones, **6 años** de serie histórica y **5 indicadores adicionales** de BEN 2025.
- **10 registros** de evidencia regulatoria en una tabla separada del dominio BEN.

La extracción fuente cubre el par 2019–2020 de BEN 2020 y pares interanuales hasta 2024–2025 de BEN 2025. Las tablas consolidadas del artículo comienzan en BEN 2021.

## Archivos

| Ruta | Contenido |
| --- | --- |
| `db/ben_electricidad.sqlite` | Base SQLite lista para descargar y consultar. |
| `data/editions.csv` | Ediciones, institución y referencias de fuente. |
| `data/source/published_comparisons.csv` | Transcripción por renglón de los cuadros comparativos publicados. |
| `data/observations/edition_observations.csv` | Observaciones de balance por edición, año de referencia y variable. |
| `data/derived/annual_comparisons.csv` | Comparaciones interanuales utilizadas en el análisis. |
| `data/derived/historical_latest_series.csv` | Último dato disponible por año de referencia. |
| `data/derived/revision_audit.csv` | Cambios de valores entre ediciones para un mismo año. |
| `data/derived/ben2025_indicators.csv` | Indicadores adicionales de la edición BEN 2025. |
| `data/derived/results.json` | Resultados decimales completos y notas metodológicas del análisis. |
| `data/context/evidencia_regulatoria.csv` | Evidencia regulatoria relacionada con el artículo, separada de los datos energéticos. |
| `sources/extraccion_BEN_electricidad_graficos.xlsx` | Planilla fuente entregada, conservada para trazabilidad. |
| `schema.sql` | Esquema relacional de SQLite. |

## Estructura de la base SQLite

| Tabla | Filas iniciales | Uso |
| --- | ---: | --- |
| `editions` | 6 | Metadatos de las ediciones y sus fuentes. |
| `published_comparisons` | 107 | Valores publicados en cada cuadro, con rótulos, signos y localizadores de origen. |
| `edition_observations` | 60 | Valores de balance conservando la edición que los publica y el año que describen. |
| `annual_comparisons` | 38 | Pares de niveles usados para comparar años consecutivos. |
| `historical_latest_series` | 6 | Serie que selecciona la edición más reciente para cada año. |
| `revision_audit` | 24 | Diferencias entre vintages de una misma variable y año. |
| `ben2025_indicators` | 5 | Indicadores adicionales publicados o analizados para BEN 2025. |
| `comparison_results` | 5 | Resultados calculados por comparación, incluidos componentes desglosados en JSON. |
| `summary_metrics` | 5 | Indicadores resumen guardados como métricas escalares. |
| `regulatory_evidence` | 10 | Evidencia documental regulatoria, con límites de inferencia. |

Las salidas derivadas mantienen su procedencia y su tabla de origen. `published_comparisons` conserva los signos con que se transcribieron los renglones del BEN. `edition_observations` utiliza las magnitudes positivas adoptadas por el análisis para cerrar el balance eléctrico.

## Consulta rápida

Con SQLite instalado:

```sql
SELECT edition_id, base_year, end_year, indicator_code,
       value_base_gwh, value_end_gwh, published_change_percent
FROM published_comparisons
WHERE edition_id = 'BEN2025'
ORDER BY indicator_code;
```

Para consultar la generación por edición y año de referencia:

```sql
SELECT edition_id, reference_year, value, unit, locator, status
FROM edition_observations
WHERE indicator_code = 'generation'
ORDER BY reference_year, edition_id;
```

Para ver revisiones del consumo final:

```sql
SELECT reference_year, from_edition_id, from_value_gwh,
       to_edition_id, to_value_gwh, change_gwh, note
FROM revision_audit
WHERE indicator_code = 'consumption'
ORDER BY reference_year, from_edition_id;
```

## Reconstruir la base

Se requiere Python 3. El generador utiliza solo la biblioteca estándar.

```bash
python scripts/build_database.py
```

El comando vuelve a exportar `Datos BEN` desde el libro fuente, genera `data/source/published_comparisons.csv` y reconstruye `db/ben_electricidad.sqlite` desde los CSV del repositorio y `results.json`.

## Procedencia y tratamiento

- Los PDF oficiales no se redistribuyen aquí. `editions.csv` enlaza al catálogo del Viceministerio de Minas y Energía y a los documentos oficiales disponibles.
- La planilla fuente y sus transcripciones se preservan. La exportación CSV redondea los valores GWh a una décima y los porcentajes a dos decimales para retirar residuos de coma flotante de Excel; la planilla original se mantiene en `sources/`.
- Los campos vacíos se mantienen vacíos. No se convierten en cero.
- Los cambios interanuales se calculan dentro de la edición que publica cada par. La tabla `historical_latest_series` selecciona el último vintage disponible por año; no debe usarse para encadenar una única tasa anual porque ediciones posteriores revisan años previos.
- El BEN 2023 amplía la cobertura de generación y actualiza valores anteriores. BEN 2024 y BEN 2025 también revisan datos de años previos. Las diferencias de revisión están en `revision_audit`.
- El detalle sectorial comparable del análisis cubre 2023–2025. Las categorías y la cobertura cambian en ediciones anteriores.
- El cierre del balance admite una tolerancia de hasta 0,3 GWh por redondeo, según la metodología documentada en el material de análisis.
- BEN 2020 contiene filas cuyo localizador de página impresa está pendiente de cotejo. El enlace directo a los PDF de BEN 2020 y BEN 2021 no estuvo disponible al preparar este repositorio; se conserva el enlace al catálogo oficial y la referencia guardada en la extracción.
- La evidencia regulatoria no constituye un inventario exhaustivo ni una auditoría legal. Sus límites figuran fila por fila.

## Fuentes oficiales

- [Catálogo histórico del BEN, Viceministerio de Minas y Energía](https://minasyenergia.mopc.gov.py/index.php?FontSize=font-large&Itemid=816&id=2069&option=com_content&view=article)
- [BEN 2022, resumen estadístico](https://minasyenergia.mopc.gov.py/pdf/balance2022/BEN%202022_Estadistico_VF.pdf)
- [BEN 2023, informe y resumen estadístico](https://minasyenergia.mopc.gov.py/pdf/balance2023/BEN%202023_Analitico%20VF.pdf)
- [BEN 2024, informe y resumen estadístico](https://minasyenergia.mopc.gov.py/pdf/balance2024/BEN%202024_Paraguay.pdf)
- [Comunicación del MOPC sobre los resultados de BEN 2025](https://mopc.gov.py/consumo-de-electricidad-supera-por-primera-vez-al-de-biomasa-solida-en-2025/)

## Repositorio GitHub

El proyecto se publica en [Br1Sanabria/ben-electricity-paraguay](https://github.com/Br1Sanabria/ben-electricity-paraguay), un repositorio público. Esta copia incluye la base SQLite, los CSV de consulta, el esquema, los scripts de reconstrucción y los insumos conservados para trazabilidad.
