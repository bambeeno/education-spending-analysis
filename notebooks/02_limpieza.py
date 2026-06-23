"""
02_limpieza.py — Limpieza y normalización del dataset de gasto educativo (UNESCO UIS)
=======================================================================================

Principios de esta etapa (ver docs/notas_contextuales.md para el detalle):
- NO se elimina ni se imputa ningún valor, incluidos casos especiales (MAGNITUDE=NIL,
    outliers como Micronesia 1972). Los huecos y anomalías pueden ser parte del dato,
    no ruido a descartar sin criterio.
- Se agregan columnas de flag explícitas para que cualquier filtro posterior sea una
    decisión consciente en la etapa de análisis, no algo escondido acá.
- Nombres de columnas a snake_case, consistente con el Proyecto 1 (HDI).
"""

import pandas as pd
from pathlib import Path

base_dir = Path(__file__).parent.parent
data_dir = base_dir / "data"
output_dir = base_dir / "output"

print("\n" + "="*80)
print("LIMPIEZA — GASTO PÚBLICO EN EDUCACIÓN (UNESCO UIS)")
print("="*80)

# ============================================================================
# 1. CARGAR EL SUBSET YA FILTRADO (output de 01_exploracion.py)
# ============================================================================
print("\n📁 Cargando subset filtrado (XGDP.FSGOV)...")
df = pd.read_csv(output_dir / "01_xgdp_fsgov_filtered.csv", low_memory=False)
print(f"   ✓ Cargado: {len(df):,} filas")

# ============================================================================
# 2. CARGAR TABLA DE PAÍSES PARA INCORPORAR NOMBRE LEGIBLE
# ============================================================================
print("\n📋 Cruzando con SDG_COUNTRY.csv para nombre de país...")
df_countries = pd.read_csv(data_dir / "SDG_COUNTRY.csv")
df = df.merge(df_countries, on="COUNTRY_ID", how="left")

sin_nombre = df["COUNTRY_NAME_EN"].isna().sum()
print(f"   ✓ Cruzado. Países sin nombre encontrado: {sin_nombre}")
if sin_nombre > 0:
    print(f"   ⚠️  COUNTRY_ID sin match: {df.loc[df['COUNTRY_NAME_EN'].isna(), 'COUNTRY_ID'].unique()}")

# ============================================================================
# 3. RENOMBRAR COLUMNAS A SNAKE_CASE
# ============================================================================
print("\n🔤 Normalizando nombres de columnas a snake_case...")

df = df.rename(columns={
    "INDICATOR_ID": "indicator_id",
    "COUNTRY_ID": "country_code",
    "COUNTRY_NAME_EN": "country_name",
    "YEAR": "year",
    "VALUE": "value_pct_gdp",
    "MAGNITUDE": "magnitude",
    "QUALIFIER": "qualifier",
    "INDICATOR_LABEL_EN": "indicator_label",
})

print(f"   ✓ Columnas finales: {list(df.columns)}")

# ============================================================================
# 4. FLAGS EXPLÍCITOS (sin eliminar ni imputar nada)
# ============================================================================
print("\n🚩 Agregando flags explícitos...")

# Flag: el valor viene marcado como NIL por la fuente (ver docs/notas_contextuales.md)
df["flag_magnitude_nil"] = df["magnitude"] == "NIL"

# Flag: el valor es una estimación (de UIS o nacional), no un dato reportado directo
df["flag_es_estimacion"] = df["qualifier"].isin(["UIS_EST", "NAT_EST"])

# Flag: outlier estadístico simple (> media + 3 desvíos estándar)
media = df["value_pct_gdp"].mean()
std = df["value_pct_gdp"].std()
umbral_outlier = media + 3 * std
df["flag_outlier_3std"] = df["value_pct_gdp"] > umbral_outlier

print(f"   ✓ flag_magnitude_nil: {df['flag_magnitude_nil'].sum()} fila(s)")
print(f"   ✓ flag_es_estimacion: {df['flag_es_estimacion'].sum()} fila(s)")
print(f"   ✓ flag_outlier_3std (umbral {umbral_outlier:.2f}%): {df['flag_outlier_3std'].sum()} fila(s)")

# ============================================================================
# 5. VALIDACIONES FINALES
# ============================================================================
print("\n✅ Validaciones finales...")

assert df["value_pct_gdp"].isna().sum() == 0, "Hay nulos en value_pct_gdp — no esperado"
assert df.duplicated(subset=["country_code", "year"]).sum() == 0, "Hay duplicados país-año"
assert df["year"].dtype == "int64", "year no es int"

print("   ✓ Sin nulos en value_pct_gdp")
print("   ✓ Sin duplicados país-año")
print("   ✓ Tipos de datos correctos")

# Orden de columnas final, prolijo
columnas_finales = [
    "country_code", "country_name", "year", "value_pct_gdp",
    "magnitude", "qualifier",
    "flag_magnitude_nil", "flag_es_estimacion", "flag_outlier_3std",
    "indicator_id", "indicator_label",
]
df = df[columnas_finales].sort_values(["country_name", "year"]).reset_index(drop=True)

# ============================================================================
# 6. EXPORTAR
# ============================================================================
print("\n💾 Exportando dataset limpio...")
out_path = output_dir / "02_education_spending_clean.csv"
df.to_csv(out_path, index=False)
print(f"   ✓ Guardado en: {out_path}")
print(f"   Shape final: {df.shape}")

print("\n" + "="*80)
print("✅ LIMPIEZA COMPLETADA")
print("="*80)
print("\nNotas:")
print("   - Ningún valor fue eliminado ni imputado.")
print("   - Casos especiales (Turquía 1998, Micronesia 1972) quedan marcados")
print("     con flags, no removidos. Ver docs/notas_contextuales.md.")
print("\nPróxima etapa: 03_analisis.py")
print("\n")