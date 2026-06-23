"""
04_exportar.py — Exportación a Excel con resumen ejecutivo
===========================================================

Inputs:
    output/02_education_spending_clean.csv
    output/03_estadisticas_descriptivas.csv
    output/03_tendencia_mundial.csv
    output/03_ranking_paises.csv

Outputs:
    output/04_resumen_ejecutivo.xlsx  — Excel con 6 hojas
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

# ============================================================================
# CONFIGURACIÓN
# ============================================================================
base_dir = Path(__file__).parent.parent
output_dir = base_dir / "output"

print("\n" + "="*80)
print("EXPORTACIÓN — RESUMEN EJECUTIVO (UNESCO UIS)")
print("="*80)

# ============================================================================
# CARGA
# ============================================================================
print("\n📁 Cargando datasets...")
df_clean = pd.read_csv(output_dir / "02_education_spending_clean.csv")
stats = pd.read_csv(output_dir / "03_estadisticas_descriptivas.csv",
                    index_col=0, header=0)
stats.index.name = "métrica"
stats.columns = ["valor"]
tendencia = pd.read_csv(output_dir / "03_tendencia_mundial.csv")
ranking = pd.read_csv(output_dir / "03_ranking_paises.csv")
print("   ✓ Todos los inputs cargados")

# ============================================================================
# HOJA 4 — RESUMEN POR REGIÓN
# ============================================================================
df_base = df_clean[~df_clean["flag_magnitude_nil"]].copy()
df_base["region"] = ranking.set_index("country_code")["region"].reindex(df_base["country_code"]).values

resumen_region = (
    df_base.groupby("region")
    .agg(
        n_paises=("country_code", "nunique"),
        n_observaciones=("value_pct_gdp", "count"),
        promedio_pct_gdp=("value_pct_gdp", "mean"),
        mediana_pct_gdp=("value_pct_gdp", "median"),
        desvio_std=("value_pct_gdp", "std"),
        minimo=("value_pct_gdp", "min"),
        maximo=("value_pct_gdp", "max"),
        primer_anio=("year", "min"),
        ultimo_anio=("year", "max"),
    )
    .reset_index()
    .sort_values("promedio_pct_gdp", ascending=False)
    .reset_index(drop=True)
)
for col in ["promedio_pct_gdp", "mediana_pct_gdp", "desvio_std", "minimo", "maximo"]:
    resumen_region[col] = resumen_region[col].round(3)

# ============================================================================
# HOJA 5 — CASOS ESPECIALES DOCUMENTADOS
# ============================================================================
casos_especiales = pd.DataFrame([
    {
        "país": "Türkiye",
        "country_code": "TUR",
        "año": 1998,
        "valor_pct_gdp": None,
        "flag": "flag_magnitude_nil",
        "categoría": "Dato NIL",
        "resumen_contexto": (
            "MAGNITUDE=NIL reportado por UNESCO UIS. Coincide con año de fuerte "
            "inestabilidad institucional: crisis diplomática con Siria (caso Öcalan), "
            "ilegalización del partido Refah tras el golpe posmoderno de 1997, y "
            "gobiernos de coalición débiles. Probable artefacto administrativo, "
            "no gasto real de 0%."
        ),
    },
    {
        "país": "Micronesia (Federated States of)",
        "country_code": "FSM",
        "año": 1972,
        "valor_pct_gdp": 66.90,
        "flag": "flag_outlier_3std",
        "categoría": "Outlier — microestado",
        "resumen_contexto": (
            "66.90% del PIB en 1972. País bajo fideicomiso de EE.UU. (TTPI), "
            "con inyección masiva de fondos externos para infraestructura educativa "
            "dividida sobre un PIB de subsistencia casi inexistente. No es error "
            "de medición: es una limitación estructural del indicador % del PIB "
            "en economías de fideicomiso reciente."
        ),
    },
    {
        "país": "Micronesia, Kiribati, Tuvalu, Marshall Islands, Nauru",
        "country_code": "FSM / KIR / TUV / MHL / NRU",
        "año": None,
        "valor_pct_gdp": None,
        "flag": "flag_outlier_3std",
        "categoría": "Patrón — microestados Pacífico",
        "resumen_contexto": (
            "9 de 14 países con outliers >3std son microestados insulares del Pacífico. "
            "Mismo mecanismo: financiamiento externo (EE.UU., Australia, NZ) dividido "
            "sobre PIB local mínimo. Sus promedios históricos dominan el Top 10 del "
            "ranking pero no son comparables con economías convencionales. Pendiente: "
            "definir umbral mínimo de años de dato para comparaciones en Project 4."
        ),
    },
    {
        "país": "Mónaco",
        "country_code": "MCO",
        "año": None,
        "valor_pct_gdp": 1.26,
        "flag": "ninguno",
        "categoría": "Caso límite del indicador",
        "resumen_contexto": (
            "Puesto 203 en el ranking con promedio de 1.26% del PIB. No refleja "
            "bajo gasto educativo real sino PIB per cápita extremadamente alto "
            "(>USD 180,000), que deflacta cualquier gasto absoluto a un porcentaje "
            "ínfimo. Caso inverso al de los microestados del Pacífico. En Project 4 "
            "mostrará IDH altísimo con gasto aparentemente bajo — artefacto metodológico."
        ),
    },
    {
        "país": "Cuba",
        "country_code": "CUB",
        "año": None,
        "valor_pct_gdp": None,
        "flag": "flag_outlier_3std",
        "categoría": "Pendiente de investigar",
        "resumen_contexto": (
            "8 apariciones como outlier entre 2005 y 2020 (10.5–14% del PIB). "
            "A diferencia de los microestados, es una economía grande y diversificada. "
            "Coherente con política de Estado que declara la educación prioridad nacional, "
            "pero falta confirmar con fuente. Gasto alto y sostenido, no un pico aislado."
        ),
    },
    {
        "país": "Lesotho, Botswana, Namibia",
        "country_code": "LSO / BWA / NAM",
        "año": None,
        "valor_pct_gdp": None,
        "flag": "flag_outlier_3std",
        "categoría": "Pendiente de investigar",
        "resumen_contexto": (
            "Varias apariciones cada uno en outliers. Posible patrón regional "
            "vinculado a políticas post-apartheid de inversión educativa en el "
            "sur de África. Hipótesis sin confirmar todavía."
        ),
    },
    {
        "país": "Cobertura global — caída fines de los 90s",
        "country_code": "Global",
        "año": None,
        "valor_pct_gdp": None,
        "flag": "ninguno",
        "categoría": "Limitación estructural del dataset",
        "resumen_contexto": (
            "Caída generalizada en cobertura de países reportantes hacia 1995-2002. "
            "Causas: crisis financiera asiática (1997-98), programas de ajuste del FMI "
            "que debilitaron capacidad estadística, y reformas metodológicas internas "
            "de UNESCO UIS. No es error del dataset. Promedios globales de ese período "
            "tienen menor representatividad que los de años adyacentes."
        ),
    },
])

# ============================================================================
# HOJA 6 — METADATOS DEL PIPELINE
# ============================================================================
metadatos = pd.DataFrame([
    {"campo": "Fecha de generación", "valor": datetime.now().strftime("%Y-%m-%d %H:%M")},
    {"campo": "Fuente primaria", "valor": "UNESCO UIS Bulk Download — SDG 4 Education (feb. 2026)"},
    {"campo": "URL fuente", "valor": "https://databrowser.uis.unesco.org/resources/bulk"},
    {"campo": "Indicador", "valor": "XGDP.FSGOV — Government expenditure on education as % of GDP"},
    {"campo": "Equivalente Banco Mundial", "valor": "SE.XPD.TOTL.GD.ZS"},
    {"campo": "Período cubierto", "valor": "1970–2025"},
    {"campo": "Países en dataset original", "valor": 206},
    {"campo": "Filas dataset original (01_exploracion)", "valor": 5159},
    {"campo": "Filas después de limpieza (02_limpieza)", "valor": 5159},
    {"campo": "Filas excluidas por flag_magnitude_nil", "valor": 1},
    {"campo": "Filas con flag_outlier_3std", "valor": 55},
    {"campo": "Filas con flag_es_estimacion", "valor": 161},
    {"campo": "Filas en df_base (análisis general)", "valor": 5158},
    {"campo": "Filas en df_tendencia (serie mundial)", "valor": 5103},
    {"campo": "Decisión: flag_magnitude_nil", "valor": "Excluidos de todo el análisis (sin valor numérico válido)"},
    {"campo": "Decisión: flag_outlier_3std", "valor": "Excluidos solo en tendencia mundial; incluidos en descriptivos y ranking"},
    {"campo": "Decisión: flag_es_estimacion", "valor": "Incluidos en todo; flag viaja al merge_ready para Project 4"},
    {"campo": "Principio metodológico central", "valor": "Ningún valor eliminado o imputado sin documentación en docs/notas_contextuales.md"},
    {"campo": "Script 01", "valor": "01_exploracion.py — filtrado del indicador, inspección, outliers"},
    {"campo": "Script 02", "valor": "02_limpieza.py — snake_case, flags explícitos"},
    {"campo": "Script 03", "valor": "03_analisis.py — estadísticas, tendencia, ranking, merge_ready"},
    {"campo": "Script 04", "valor": "04_exportar.py — este archivo, resumen ejecutivo Excel"},
    {"campo": "Script 05", "valor": "05_visualizacion.py — gráficos PNG"},
    {"campo": "Proyecto siguiente", "valor": "Project 3 — Impacto pandemia en gasto educativo global"},
    {"campo": "Proyecto 4", "valor": "Project 4 — Correlación HDI × gasto educativo"},
])

# ============================================================================
# EXPORTAR A EXCEL
# ============================================================================
print("\n💾 Exportando Excel...")
out_path = output_dir / "04_resumen_ejecutivo.xlsx"

with pd.ExcelWriter(out_path, engine="openpyxl") as writer:

    # Hoja 1 — Estadísticas descriptivas
    stats.reset_index().to_excel(writer, sheet_name="1_Estadísticas", index=False)

    # Hoja 2 — Tendencia mundial
    tendencia.to_excel(writer, sheet_name="2_Tendencia_mundial", index=False)

    # Hoja 3 — Ranking de países
    ranking.to_excel(writer, sheet_name="3_Ranking_países", index=False)

    # Hoja 4 — Resumen por región
    resumen_region.to_excel(writer, sheet_name="4_Resumen_región", index=False)

    # Hoja 5 — Casos especiales
    casos_especiales.to_excel(writer, sheet_name="5_Casos_especiales", index=False)

    # Hoja 6 — Metadatos
    metadatos.to_excel(writer, sheet_name="6_Metadatos_pipeline", index=False)

print(f"   ✓ Guardado en: {out_path}")
print("""
Hojas generadas:
    1_Estadísticas         — métricas descriptivas globales
    2_Tendencia_mundial    — promedio y mediana mundial por año (1970–2025)
    3_Ranking_países       — 206 países ordenados por promedio histórico
    4_Resumen_región       — agregado por región geográfica
    5_Casos_especiales     — outliers y anomalías documentadas con contexto
    6_Metadatos_pipeline   — fuente, decisiones de filtrado, data lineage
""")

print("="*80)
print("✅ EXPORTACIÓN COMPLETADA")
print("="*80)
print("\nPróxima etapa: 05_visualizacion.py — Gráficos PNG\n")