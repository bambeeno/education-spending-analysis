"""
03_analisis.py — Análisis exploratorio del gasto público en educación (UNESCO UIS)
====================================================================================

Inputs:
    output/02_education_spending_clean.csv

Outputs:
    output/03_estadisticas_descriptivas.csv
    output/03_tendencia_mundial.csv
    output/03_ranking_paises.csv
    output/03_education_spending_merge_ready.csv

Principios aplicados:
    - flag_magnitude_nil  → excluidos de todo el análisis
    - flag_outlier_3std   → excluidos solo en cálculo de tendencia mundial
    - flag_es_estimacion  → incluidos en todo, flag viaja al merge_ready
"""

import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================================
# CONFIGURACIÓN
# ============================================================================
base_dir = Path(__file__).parent.parent
output_dir = base_dir / "output"

print("\n" + "="*80)
print("ANÁLISIS EXPLORATORIO — GASTO PÚBLICO EN EDUCACIÓN (UNESCO UIS)")
print("="*80)

# ============================================================================
# 1. CARGA
# ============================================================================
print("\n📁 Cargando dataset limpio...")
df = pd.read_csv(output_dir / "02_education_spending_clean.csv")
print(f"   ✓ {len(df):,} filas | {df['country_code'].nunique()} países | "
        f"años {df['year'].min()}–{df['year'].max()}")

# ============================================================================
# 2. MAPEO DE REGIONES
# ============================================================================
print("\n🌍 Asignando regiones geográficas...")

REGION_MAP = {
    "USA": "Norteamérica", "CAN": "Norteamérica", "MEX": "Norteamérica",
    "ARG": "Latinoamérica y Caribe", "BOL": "Latinoamérica y Caribe",
    "BRA": "Latinoamérica y Caribe", "CHL": "Latinoamérica y Caribe",
    "COL": "Latinoamérica y Caribe", "CRI": "Latinoamérica y Caribe",
    "CUB": "Latinoamérica y Caribe", "DOM": "Latinoamérica y Caribe",
    "ECU": "Latinoamérica y Caribe", "GTM": "Latinoamérica y Caribe",
    "HND": "Latinoamérica y Caribe", "HTI": "Latinoamérica y Caribe",
    "JAM": "Latinoamérica y Caribe", "NIC": "Latinoamérica y Caribe",
    "PAN": "Latinoamérica y Caribe", "PER": "Latinoamérica y Caribe",
    "PRY": "Latinoamérica y Caribe", "SLV": "Latinoamérica y Caribe",
    "TTO": "Latinoamérica y Caribe", "URY": "Latinoamérica y Caribe",
    "VEN": "Latinoamérica y Caribe", "GUY": "Latinoamérica y Caribe",
    "SUR": "Latinoamérica y Caribe", "BLZ": "Latinoamérica y Caribe",
    "BRB": "Latinoamérica y Caribe", "ATG": "Latinoamérica y Caribe",
    "DMA": "Latinoamérica y Caribe", "GRD": "Latinoamérica y Caribe",
    "KNA": "Latinoamérica y Caribe", "LCA": "Latinoamérica y Caribe",
    "VCT": "Latinoamérica y Caribe", "BHS": "Latinoamérica y Caribe",
    "PRI": "Latinoamérica y Caribe",
    "ALB": "Europa", "AND": "Europa", "AUT": "Europa", "BEL": "Europa",
    "BGR": "Europa", "BIH": "Europa", "BLR": "Europa", "CHE": "Europa",
    "CYP": "Europa", "CZE": "Europa", "DEU": "Europa", "DNK": "Europa",
    "ESP": "Europa", "EST": "Europa", "FIN": "Europa", "FRA": "Europa",
    "GBR": "Europa", "GRC": "Europa", "HRV": "Europa", "HUN": "Europa",
    "IRL": "Europa", "ISL": "Europa", "ITA": "Europa", "LIE": "Europa",
    "LTU": "Europa", "LUX": "Europa", "LVA": "Europa", "MDA": "Europa",
    "MKD": "Europa", "MLT": "Europa", "MNE": "Europa", "NLD": "Europa",
    "NOR": "Europa", "POL": "Europa", "PRT": "Europa", "ROU": "Europa",
    "RUS": "Europa", "SMR": "Europa", "SRB": "Europa", "SVK": "Europa",
    "SVN": "Europa", "SWE": "Europa", "TUR": "Europa", "UKR": "Europa",
    "XKX": "Europa", "MCO": "Europa",
    "AUS": "Asia-Pacífico", "CHN": "Asia-Pacífico", "FJI": "Asia-Pacífico",
    "FSM": "Asia-Pacífico", "IDN": "Asia-Pacífico", "JPN": "Asia-Pacífico",
    "KHM": "Asia-Pacífico", "KIR": "Asia-Pacífico", "KOR": "Asia-Pacífico",
    "LAO": "Asia-Pacífico", "MHL": "Asia-Pacífico", "MMR": "Asia-Pacífico",
    "MNG": "Asia-Pacífico", "MYS": "Asia-Pacífico", "NRU": "Asia-Pacífico",
    "NZL": "Asia-Pacífico", "PHL": "Asia-Pacífico", "PLW": "Asia-Pacífico",
    "PNG": "Asia-Pacífico", "PRK": "Asia-Pacífico", "SGP": "Asia-Pacífico",
    "SLB": "Asia-Pacífico", "THA": "Asia-Pacífico", "TLS": "Asia-Pacífico",
    "TON": "Asia-Pacífico", "TUV": "Asia-Pacífico", "TWN": "Asia-Pacífico",
    "VNM": "Asia-Pacífico", "VUT": "Asia-Pacífico", "WSM": "Asia-Pacífico",
    "HKG": "Asia-Pacífico", "MAC": "Asia-Pacífico", "COK": "Asia-Pacífico",
    "BRN": "Asia-Pacífico",
    "AFG": "Asia del Sur", "BGD": "Asia del Sur", "BTN": "Asia del Sur",
    "IND": "Asia del Sur", "LKA": "Asia del Sur", "MDV": "Asia del Sur",
    "NPL": "Asia del Sur", "PAK": "Asia del Sur",
    "ARE": "Asia Central y Occidental", "ARM": "Asia Central y Occidental",
    "AZE": "Asia Central y Occidental", "BHR": "Asia Central y Occidental",
    "GEO": "Asia Central y Occidental", "IRN": "Asia Central y Occidental",
    "IRQ": "Asia Central y Occidental", "ISR": "Asia Central y Occidental",
    "JOR": "Asia Central y Occidental", "KAZ": "Asia Central y Occidental",
    "KGZ": "Asia Central y Occidental", "KWT": "Asia Central y Occidental",
    "LBN": "Asia Central y Occidental", "OMN": "Asia Central y Occidental",
    "PSE": "Asia Central y Occidental", "QAT": "Asia Central y Occidental",
    "SAU": "Asia Central y Occidental", "SYR": "Asia Central y Occidental",
    "TJK": "Asia Central y Occidental", "TKM": "Asia Central y Occidental",
    "UZB": "Asia Central y Occidental", "YEM": "Asia Central y Occidental",
    "AGO": "África Subsahariana", "BDI": "África Subsahariana",
    "BEN": "África Subsahariana", "BFA": "África Subsahariana",
    "BWA": "África Subsahariana", "CAF": "África Subsahariana",
    "CIV": "África Subsahariana", "CMR": "África Subsahariana",
    "COD": "África Subsahariana", "COG": "África Subsahariana",
    "COM": "África Subsahariana", "CPV": "África Subsahariana",
    "DJI": "África Subsahariana", "ERI": "África Subsahariana",
    "ETH": "África Subsahariana", "GAB": "África Subsahariana",
    "GHA": "África Subsahariana", "GIN": "África Subsahariana",
    "GMB": "África Subsahariana", "GNB": "África Subsahariana",
    "GNQ": "África Subsahariana", "KEN": "África Subsahariana",
    "LBR": "África Subsahariana", "LSO": "África Subsahariana",
    "MDG": "África Subsahariana", "MLI": "África Subsahariana",
    "MOZ": "África Subsahariana", "MRT": "África Subsahariana",
    "MUS": "África Subsahariana", "MWI": "África Subsahariana",
    "NAM": "África Subsahariana", "NER": "África Subsahariana",
    "NGA": "África Subsahariana", "RWA": "África Subsahariana",
    "SDN": "África Subsahariana", "SEN": "África Subsahariana",
    "SLE": "África Subsahariana", "SOM": "África Subsahariana",
    "SSD": "África Subsahariana", "STP": "África Subsahariana",
    "SWZ": "África Subsahariana", "SYC": "África Subsahariana",
    "TCD": "África Subsahariana", "TGO": "África Subsahariana",
    "TZA": "África Subsahariana", "UGA": "África Subsahariana",
    "ZAF": "África Subsahariana", "ZMB": "África Subsahariana",
    "ZWE": "África Subsahariana",
    "DZA": "África del Norte", "EGY": "África del Norte",
    "LBY": "África del Norte", "MAR": "África del Norte",
    "TUN": "África del Norte", "SDS": "África del Norte",
    "ASM": "Territorios y otros", "AIA": "Territorios y otros",
    "ABW": "Territorios y otros", "BMU": "Territorios y otros",
    "VGB": "Territorios y otros", "CYM": "Territorios y otros",
    "CUW": "Territorios y otros", "MSR": "Territorios y otros",
    "SXM": "Territorios y otros", "TCA": "Territorios y otros",
}

df["region"] = df["country_code"].map(REGION_MAP).fillna("Sin clasificar")
sin_region = df[df["region"] == "Sin clasificar"]["country_code"].nunique()
if sin_region > 0:
    codes = df[df["region"] == "Sin clasificar"]["country_code"].unique()
    print(f"   ⚠️  {sin_region} país(es) sin región asignada: {list(codes)}")
else:
    print("   ✓ Todos los países tienen región asignada")
print(df.groupby("region")["country_code"].nunique().sort_values(ascending=False).to_string(header=False))

# ============================================================================
# 3. DATASETS DE TRABAJO
# ============================================================================
print("\n🔎 Preparando datasets de trabajo...")
df_base = df[~df["flag_magnitude_nil"]].copy()
df_tendencia = df_base[~df_base["flag_outlier_3std"]].copy()
print(f"   ✓ df_base (sin NIL): {len(df_base):,} filas")
print(f"   ✓ df_tendencia (sin NIL, sin outliers 3std): {len(df_tendencia):,} filas")

# ============================================================================
# 4. ESTADÍSTICAS DESCRIPTIVAS
# ============================================================================
print("\n📊 4. Estadísticas descriptivas globales...")

stats = df_base["value_pct_gdp"].describe(percentiles=[.1, .25, .5, .75, .9])
stats_extra = pd.Series({
    "skewness": df_base["value_pct_gdp"].skew(),
    "kurtosis": df_base["value_pct_gdp"].kurt(),
    "paises_totales": df["country_code"].nunique(),
    "paises_con_dato": df_base["country_code"].nunique(),
    "anios_cubiertos": df_base["year"].nunique(),
    "filas_estimacion": int(df_base["flag_es_estimacion"].sum()),
    "filas_outlier_3std": int(df_base["flag_outlier_3std"].sum()),
    "filas_nil": int(df["flag_magnitude_nil"].sum()),
})
stats_combined = pd.concat([stats, stats_extra])
print(stats_combined.to_string())
stats_combined.to_csv(output_dir / "03_estadisticas_descriptivas.csv", header=["valor"])
print("   ✓ Guardado: 03_estadisticas_descriptivas.csv")

# ============================================================================
# 5. TENDENCIA MUNDIAL
# ============================================================================
print("\n📈 5. Calculando tendencia mundial por año...")

tendencia = (
    df_tendencia
    .groupby("year")["value_pct_gdp"]
    .agg(
        promedio_mundial="mean",
        mediana_mundial="median",
        desvio_std="std",
        n_paises="count",
    )
    .reset_index()
)
tendencia["ic_inferior"] = tendencia["promedio_mundial"] - tendencia["desvio_std"]
tendencia["ic_superior"] = tendencia["promedio_mundial"] + tendencia["desvio_std"]
tendencia.to_csv(output_dir / "03_tendencia_mundial.csv", index=False)
print(f"   ✓ Serie temporal: {len(tendencia)} años")
print("   ✓ Guardado: 03_tendencia_mundial.csv")

# ============================================================================
# 6. RANKING DE PAÍSES
# ============================================================================
print("\n🏆 6. Calculando ranking de países...")

ranking = (
    df_base
    .groupby(["country_code", "country_name", "region"])["value_pct_gdp"]
    .agg(
        promedio_historico="mean",
        mediana_historica="median",
        anios_con_dato="count",
        primer_anio="min",
        ultimo_anio="max",
    )
    .reset_index()
    .sort_values("promedio_historico", ascending=False)
    .reset_index(drop=True)
)

pct_est = df_base.groupby("country_code")["flag_es_estimacion"].mean().rename("pct_estimaciones")
ranking = ranking.merge(pct_est, on="country_code")
ranking["rank"] = range(1, len(ranking) + 1)
ranking.to_csv(output_dir / "03_ranking_paises.csv", index=False)
print(f"   ✓ {len(ranking)} países rankeados")
print("   ✓ Guardado: 03_ranking_paises.csv")

# ============================================================================
# 7. MERGE-READY PARA PROJECT 4
# ============================================================================
print("\n🔗 7. Preparando dataset merge-ready para Project 4...")

merge_ready = (
    df_base[["country_code", "country_name", "region", "year", "value_pct_gdp",
                "flag_es_estimacion", "flag_outlier_3std"]]
    .copy()
    .sort_values(["country_code", "year"])
    .reset_index(drop=True)
)
merge_ready.to_csv(output_dir / "03_education_spending_merge_ready.csv", index=False)
print(f"   ✓ Shape: {merge_ready.shape}")
print("   ✓ Guardado: 03_education_spending_merge_ready.csv")

# ============================================================================
# RESUMEN FINAL
# ============================================================================
print("\n" + "="*80)
print("✅ ANÁLISIS COMPLETADO")
print("="*80)
print("""
Outputs generados en output/:
    03_estadisticas_descriptivas.csv
    03_tendencia_mundial.csv
    03_ranking_paises.csv
    03_education_spending_merge_ready.csv

Próximas etapas:
    04_exportar.py  — Excel con resumen ejecutivo
    05_visualizacion.py — Gráficos
""")