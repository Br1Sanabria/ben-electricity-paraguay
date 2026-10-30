"""English translations for source labels and analysis metadata."""

import unicodedata

PUBLISHER_TRANSLATIONS = {
    "Viceministerio de Minas y Energía - MOPC": "Vice Ministry of Mines and Energy - MOPC",
}

REPORT_TITLE_TRANSLATIONS = {
    f"Balance Energético Nacional {year}": f"National Energy Balance (BEN) {year}"
    for year in range(2020, 2026)
}

EDITION_NOTE_TRANSLATIONS = {
    "La edición incorpora ajustes metodológicos; los años de referencia conservan su edición de origen.": "This edition applies methodological adjustments; each reference year remains tied to the edition that reports it.",
    "La edición publica cuadros bajo SIEN y siePARAGUAY.": "This edition publishes tables under SIEN and siePARAGUAY.",
    "La edición se consulta desde el catálogo histórico oficial.": "This edition is available through the official historical catalog.",
    "La extracción marca el corte 31-07-2021; en varias filas la página impresa figura pendiente de cotejo.": "The extraction lists a 2021-07-31 cutoff; printed page numbers for several rows still require verification.",
    "La fuente suministrada incluye la extracción de los cuadros; source_url apunta a la comunicación oficial del MOPC sobre la presentación del BEN 2025.": "The supplied source includes the transcribed tables; source_url points to the official MOPC announcement of the BEN 2025 presentation.",
    "El informe declara preliminares los datos de 2024.": "The report identifies 2024 data as preliminary.",
}

LABEL_TRANSLATIONS = {
    "└ Binacionales": "└ Binational hydropower plants",
    "└ CHE Acaray": "└ Acaray Hydroelectric Power Plant",
    "└ Distribución": "└ Distribution",
    "└ Térmica": "└ Thermal",
    "└ Transmisión": "└ Transmission",
    "Alumbrado público": "Public lighting",
    "Alumbrado público y otros": "Public lighting and other",
    "ANDE": "ANDE",
    "Autoproductores": "Autoproducers",
    "Binacionales": "Binational hydropower plants",
    "Centrales eléctricas": "Power plants",
    "CHE Acaray": "Acaray Hydroelectric Power Plant",
    "Comercial": "Commercial",
    "Comercial y servicios públicos": "Commercial and public services",
    "Consumo en centrales / autoconsumo ANDE": "Power-plant consumption / ANDE self-consumption",
    "Consumo en centrales/ autoconsumo ANDE": "Power-plant consumption / ANDE self-consumption",
    "Consumo en centrales/autoconsumo ANDE": "Power-plant consumption / ANDE self-consumption",
    "Consumo en centrales y autoconsumo ANDE": "Power-plant consumption and ANDE self-consumption",
    "CONSUMO FINAL": "FINAL CONSUMPTION",
    "Consumo final": "Final consumption",
    "Consumo propio": "Own use",
    "Consumo de Infraestructura Digital Avanzada": "Advanced Digital Infrastructure consumption",
    "Demanda máxima de potencia": "Peak power demand",
    "Distribución": "Distribution",
    "Exportación": "Exports",
    "Exportación (magnitud positiva)": "Exports (positive magnitude)",
    "Exportaciones a Argentina": "Exports to Argentina",
    "Exportaciones a Brasil": "Exports to Brazil",
    "Generación Bruta": "Gross generation",
    "Generación bruta": "Gross generation",
    "Generación solar": "Solar generation",
    "Hidroeléctrica + Solar": "Hydropower + Solar",
    "Importación": "Imports",
    "Industria": "Industry",
    "Industrial": "Industrial",
    "OFERTA": "SUPPLY",
    "OFERTA / DEMANDA INTERNA": "SUPPLY / DOMESTIC DEMAND",
    "Otros no especificados": "Other unspecified",
    "Otros sectores": "Other sectors",
    "Pérdidas": "Losses",
    "Pérdidas Totales": "Total losses",
    "Público y otros": "Public and other",
    "Público y otros *": "Public and other *",
    "Residencial": "Residential",
    "Térmica": "Thermal",
    "Transmisión": "Transmission",
}


def normalize_label(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    without_marks = "".join(char for char in normalized if not unicodedata.combining(char))
    return " ".join(without_marks.casefold().split())


NORMALIZED_LABEL_TRANSLATIONS = {
    normalize_label(label): translation
    for label, translation in LABEL_TRANSLATIONS.items()
}


def translate_label(value: str) -> str:
    if value in LABEL_TRANSLATIONS:
        return LABEL_TRANSLATIONS[value]
    normalized = normalize_label(value)
    if normalized in NORMALIZED_LABEL_TRANSLATIONS:
        return NORMALIZED_LABEL_TRANSLATIONS[normalized]
    raise ValueError(f"Missing English translation for published label: {value}")

PUBLISHED_PAGE_TRANSLATIONS = {
    "Cotejar página impresa": "Verify printed page",
}

PUBLISHED_NOTE_TRANSLATIONS = {
    f"Preliminar; corte 31-07-{year}": f"Preliminary; cutoff {year}-07-31"
    for year in range(2021, 2027)
}

LOCATOR_TRANSLATIONS = {
    "Comparativo del balance de electricidad; p. 9": "Electricity balance comparison; p. 9",
    "Comparativo del balance de electricidad; p. 14": "Electricity balance comparison; p. 14",
    "Cuadro 3; p. 28": "Table 3; p. 28",
    "Cuadro 3; p. 48": "Table 3; p. 48",
    "Cuadro 3; p. 49": "Table 3; p. 49",
    "Aspectos relevantes; p. 17": "Key highlights; p. 17",
    "Detalle de exportación; p. 22": "Exports detail; p. 22",
    "Valoración de otros sectores; p. 30": "Assessment of other sectors; p. 30",
    "Art. 1: modificación del art. 4 de Ley 3009": "Article 1: amendment to Article 4 of Law 3009",
    "Art. 1: modificaciones de arts. 4; 24; 25": "Article 1: amendments to Articles 4, 24, and 25",
    "Art. 7": "Article 7",
    "Arts. 24 a 26": "Articles 24–26",
    "Arts. 28 y 29": "Articles 28 and 29",
    "Comunicación ANDE de 19 de mayo de 2026": "ANDE communication dated 19 May 2026",
    "Índice VMME: objeto de Resolución 994/2026": "VMME index: subject of Resolution 994/2026",
    "Índice VMME: objeto de Resolución 995/2026": "VMME index: subject of Resolution 995/2026",
    "Índice VMME: objeto de Resolución 996/2026": "VMME index: subject of Resolution 996/2026",
    "Sin base de expedientes y proyectos en este estudio": "Case and project records were outside this study",
}

STATUS_TRANSLATIONS = {
    "Año 2021 preliminar; corte de información 31-07-2022.": "2021 preliminary; data cutoff 2022-07-31.",
    "Año 2022 preliminar; corte 31-07-2023; cuadro bajo serie SIEN.": "2022 preliminary; cutoff 2023-07-31; table follows the SIEN series.",
    "Año 2022 reexpresado bajo siePARAGUAY; generación bruta incluye autoproductores.": "2022 values restated under siePARAGUAY; gross generation includes autoproducers.",
    "Año 2023 preliminar; corte de información 31-07-2024.": "2023 preliminary; data cutoff 2024-07-31.",
    "Año 2024 preliminar; corte de información 31-07-2025.": "2024 preliminary; data cutoff 2025-07-31.",
    "Año 2025 preliminar; corte de información 31-07-2026.": "2025 preliminary; data cutoff 2026-07-31.",
    "Valor comparativo BEN 2022; coincide con BEN 2021.": "Comparative value in BEN 2022; matches BEN 2021.",
    "Valor de 2024 revisado en la edición BEN 2025.": "2024 value revised in the BEN 2025 edition.",
    "Valor publicado en BEN 2021; balance comparativo 2021–2020.": "Value published in BEN 2021; 2021–2020 comparative balance.",
    "Valores agregados de 2023 reproducidos en BEN 2024.": "2023 aggregate values reproduced in BEN 2024.",
}

REVISION_NOTE_TRANSLATIONS = {
    "BEN 2023 presenta el año 2022 bajo siePARAGUAY e incluye autoproductores en generación bruta; el cambio no debe leerse solo como revisión estadística.": "BEN 2023 reports 2022 under siePARAGUAY and includes autoproducers in gross generation; the change should not be read as a statistical revision alone.",
    "BEN 2025 revisa los flujos de 2024; actualiza, entre otros insumos, la estimación residencial.": "BEN 2025 revises 2024 flows, including an updated residential estimate.",
    "Los agregados de 2023 se reproducen sin cambios en BEN 2024.": "The 2023 aggregates are reproduced unchanged in BEN 2024.",
    "Los valores de 2021 coinciden entre BEN 2021 y BEN 2022.": "The 2021 values match in BEN 2021 and BEN 2022.",
}

REGULATORY_FUNCTION_TRANSLATIONS = {
    "Acceso institucional": "Institutional access",
    "Acceso y coordinación": "Access and coordination",
    "Conexión y operación": "Connection and operation",
    "Contratación": "Procurement",
    "Desarrollo procedimental": "Procedural development",
    "Desempeño": "Performance",
    "Riesgo de entrega": "Delivery risk",
}

REGULATORY_OBSERVATION_TRANSLATIONS = {
    "Acreditación de restricciones y criterios de remuneración": "Evidence of constraints and compensation criteria",
    "Autoridad de aplicación MOPC/VMME": "Regulatory authority: MOPC/VMME",
    "Autoridad MOPC/VMME y exigencias técnicas vinculadas con ANDE": "MOPC/VMME authority and technical requirements involving ANDE",
    "Cantidad de energía y restricciones técnicas u operativas": "Energy volumes and technical or operational constraints",
    "Confirmación institucional de reglamentación": "Institutional confirmation of implementing regulations",
    "Exigencias técnicas y reglas de despacho": "Technical requirements and dispatch rules",
    "Horizonte contractual y procedimiento de precios": "Contract term and pricing procedure",
    "No se evaluaron resultados operativos": "Operational outcomes were not evaluated",
    "Procedimiento de elaboración del precio de referencia unitario": "Procedure for calculating the unit reference price",
    "Requisitos y procedimiento de solicitudes de licencias": "Licensing application requirements and process",
}

INFERENCE_LIMIT_TRANSLATIONS = {
    "No demuestra adjudicación ni cierre financiero": "Does not demonstrate contract award or financial close",
    "No identifica capacidad disponible ni costos de conexión": "Does not identify available capacity or connection costs",
    "No mide calidad de coordinación": "Does not measure coordination quality",
    "No mide energía restringida ni compensación efectivamente pagada": "Does not measure curtailed energy or compensation actually paid",
    "No mide independencia efectiva ni tiempos de tramitación": "Does not measure effective independence or processing times",
    "No se auditaron anexos ni aplicación": "Appendices and implementation were not audited",
    "No se auditaron anexos ni tiempos reales": "Appendices and actual timelines were not audited",
    "No se auditaron anexos ni valores aplicados": "Appendices and applied values were not audited",
    "No se auditó el articulado completo ni los anexos del decreto": "The full legal text and decree appendices were not audited",
    "No significa inexistencia de proyectos ni incumplimiento": "Does not imply that projects do not exist or that requirements were breached",
}

RESULT_COMPONENT_TRANSLATIONS = {
    "Cambio de generación": "Generation change",
    "Cambio de consumo final": "Final consumption change",
    "Cambio de pérdidas": "Losses change",
    "Cambio de consumo propio": "Own use change",
    "Cambio de importaciones": "Imports change",
    "Cambio del residuo": "Residual change",
}
