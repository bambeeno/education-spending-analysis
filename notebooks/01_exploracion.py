"""
01_exploracion.py — Inspección inicial del dataset UNESCO UIS de gasto público en educación
==========================================================================================

Objetivo: entender la estructura del dataset nativo de UNESCO (formato long/tidy),
confirmar el rango de años, cobertura, nulos, outliers, antes de limpiar.

Dataset: SDG_DATA_NATIONAL.csv + SDG_LABEL.csv + SDG_COUNTRY.csv
Indicador filtrado: XGDP.FSGOV = "Government expenditure on education as a percentage of GDP (%)"
"""

import pandas as pd
from pathlib import Path

# Rutas relativas portables (mismo patrón que Proyecto 1)
base_dir = Path(__file__).parent.parent
data_dir = base_dir / "data"
output_dir = base_dir / "output"

print("\n" + "="*80)
print("EXPLORACIÓN INICIAL — GASTO PÚBLICO EN EDUCACIÓN (UNESCO UIS)")
print("="*80)

# ============================================================================
# 1. CARGAR EL ARCHIVO PRINCIPAL (NACIONAL)
# ============================================================================
print("\n📁 Cargando SDG_DATA_NATIONAL.csv...")
print("   (Esto puede tomar unos segundos, son ~1.46M filas)")

df_national = pd.read_csv(
    data_dir / "SDG_DATA_NATIONAL.csv",
    low_memory=False
)

print(f"   ✓ Cargado: {len(df_national):,} filas, {df_national.shape[1]} columnas")
print(f"   Columnas: {list(df_national.columns)}")

# ============================================================================
# 2. FILTRAR SOLO EL INDICADOR QUE NOS INTERESA
# ============================================================================
print("\n🔍 Filtrando indicador XGDP.FSGOV (Government expenditure on education % GDP)...")

df = df_national[df_national['INDICATOR_ID'] == 'XGDP.FSGOV'].copy()
print(f"   ✓ Filas encontradas: {len(df):,}")

# ============================================================================
# 3. CARGAR LABELS Y METADATA ACOMPAÑANTE
# ============================================================================
print("\n📋 Cargando metadata...")

df_labels = pd.read_csv(data_dir / "SDG_LABEL.csv")
df_countries = pd.read_csv(data_dir / "SDG_COUNTRY.csv")

# Cruzar con labels para tener descripción del indicador
df = df.merge(
    df_labels,
    left_on='INDICATOR_ID',
    right_on='INDICATOR_ID',
    how='left'
)

# Cruzar con países para tener nombres en lugar de códigos (solo para exploración)
df_explore = df.merge(
    df_countries,
    left_on='COUNTRY_ID',
    right_on='COUNTRY_ID',
    how='left'
)

print(f"   ✓ Labels cruzados")
print(f"   ✓ Nombres de países agregados para exploración")

# ============================================================================
# 4. INSPECCIÓN BÁSICA
# ============================================================================
print("\n" + "-"*80)
print("INSPECCIÓN BÁSICA")
print("-"*80)

print(f"\n📊 Shape: {df.shape}")
print(f"\n🌍 Países únicos: {df['COUNTRY_ID'].nunique()}")
print(f"📅 Años: {df['YEAR'].min()} – {df['YEAR'].max()} (rango: {df['YEAR'].max() - df['YEAR'].min() + 1} años)")
print(f"📈 Valores de gasto % GDP:")
print(f"   Min: {df['VALUE'].min():.2f}%")
print(f"   Max: {df['VALUE'].max():.2f}%")
print(f"   Media: {df['VALUE'].mean():.2f}%")
print(f"   Mediana: {df['VALUE'].median():.2f}%")
print(f"   Std: {df['VALUE'].std():.2f}%")

# ============================================================================
# 5. NULOS Y VALORES ESPECIALES (MAGNITUDE, QUALIFIER)
# ============================================================================
print(f"\n🔲 Nulos en VALUE: {df['VALUE'].isna().sum()} / {len(df)}")
print(f"   MAGNITUDE (valores especiales):")
for mag in df['MAGNITUDE'].dropna().unique():
    count = (df['MAGNITUDE'] == mag).sum()
    print(f"      {mag}: {count} registros")

print(f"   QUALIFIER (calidad del dato):")
for qual in df['QUALIFIER'].dropna().unique():
    count = (df['QUALIFIER'] == qual).sum()
    print(f"      {qual}: {count} registros")

# ============================================================================
# 6. COBERTURA POR AÑO
# ============================================================================
print(f"\n📅 Cobertura (cantidad de países con dato) por año:")
cobertura = df.groupby('YEAR')['COUNTRY_ID'].nunique()

print(f"\n   Décadas (primeros 3 años de cada década):")
for decade in range(1970, 2030, 10):
    years_in_range = [y for y in cobertura.index if decade <= y < decade + 3]
    subset = cobertura.loc[years_in_range]
    if len(subset) > 0:
        print(f"      {decade}s: {subset.values}")

print(f"\n   Últimos 10 años:")
print(cobertura.tail(10))

# ============================================================================
# 7. OUTLIERS POTENCIALES (> 20% del PBI es muy alto)
# ============================================================================
print(f"\n⚠️  Potenciales outliers (gasto > 20% del PBI):")
outliers = df_explore[df['VALUE'] > 20].sort_values('VALUE', ascending=False)
if len(outliers) > 0:
    print(f"   {len(outliers)} registros encontrados:")
    for idx, row in outliers.head(10).iterrows():
        print(f"      {row['COUNTRY_NAME_EN']} ({row['COUNTRY_ID']}) {row['YEAR']}: {row['VALUE']:.2f}%")
else:
    print(f"   Ninguno encontrado")

# ============================================================================
# 8. PRIMERAS Y ÚLTIMAS FILAS (MUESTRA)
# ============================================================================
print(f"\n📋 Primeras 5 filas:")
print(df_explore[['COUNTRY_NAME_EN', 'COUNTRY_ID', 'YEAR', 'VALUE', 'MAGNITUDE', 'QUALIFIER']].head())

print(f"\n📋 Últimas 5 filas:")
print(df_explore[['COUNTRY_NAME_EN', 'COUNTRY_ID', 'YEAR', 'VALUE', 'MAGNITUDE', 'QUALIFIER']].tail())

# ============================================================================
# 9. GUARDADO INTERMEDIO
# ============================================================================
print(f"\n💾 Guardando subset filtrado...")
df.to_csv(output_dir / "01_xgdp_fsgov_filtered.csv", index=False)
print(f"   ✓ Guardado en: {output_dir / '01_xgdp_fsgov_filtered.csv'}")

print("\n" + "="*80)
print("✅ EXPLORACIÓN COMPLETADA")
print("="*80)
print("\nPróxima etapa: 02_limpieza.py")
print("   - Transformación wide → long (si es necesaria)")
print("   - Limpieza de tipos de datos")
print("   - Exportación final para análisis")
print("\n")