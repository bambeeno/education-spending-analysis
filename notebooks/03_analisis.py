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
    output/figures/03_distribucion_gasto.png
    output/figures/03_tendencia_mundial.png
    output/figures/03_top_bottom_paises.png
    output/figures/03_cobertura_temporal.png

Principios aplicados:
    - flag_magnitude_nil  → excluidos de todo el análisis
    - flag_outlier_3std   → excluidos solo en cálculo de tendencia mundial
    - flag_es_estimacion  → incluidos en todo, flag viaja al merge_ready
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from pathlib import Path

# ============================================================================
# CONFIGURACIÓN
# ============================================================================
base_dir = Path(__file__).parent.parent
output_dir = base_dir / "output"
figures_dir = output_dir / "figures"
figures_dir.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    "figure.dpi": 150,
    "figure.facecolor": "white",
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
    "axes.labelsize": 11,
})

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
print(f"   ✓ Distribución:")
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
print(f"\n   TOP 10:")
print(ranking[["rank","country_name","region","promedio_historico","anios_con_dato"]].head(10).to_string(index=False))
print(f"\n   BOTTOM 10:")
print(ranking[["rank","country_name","region","promedio_historico","anios_con_dato"]].tail(10).to_string(index=False))
print("   ✓ Guardado: 03_ranking_paises.csv")

# ============================================================================
# 7. MERGE-READY PARA PROJECT 3
# ============================================================================
print("\n🔗 7. Preparando dataset merge-ready para Project 3...")

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
# 8. GRÁFICOS
# ============================================================================
print("\n🎨 8. Generando gráficos...")

# 8.1 Distribución
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

ax1 = axes[0]
sns.histplot(data=df_base, x="value_pct_gdp", bins=60, kde=True,
                color="#2196F3", alpha=0.7, ax=ax1)
ax1.axvline(df_base["value_pct_gdp"].median(), color="#E53935", lw=1.8,
            linestyle="--", label=f"Mediana: {df_base['value_pct_gdp'].median():.2f}%")
ax1.axvline(df_base["value_pct_gdp"].mean(), color="#FB8C00", lw=1.8,
            linestyle="-.", label=f"Promedio: {df_base['value_pct_gdp'].mean():.2f}%")
ax1.set_title("Distribución del gasto en educación")
ax1.set_xlabel("% del PIB")
ax1.set_ylabel("Observaciones(Frecuencia)")
ax1.legend()

ax2 = axes[1]
region_orden = (df_base.groupby("region")["value_pct_gdp"].median()
                .sort_values().index.tolist())
sns.boxplot(data=df_base, y="region", x="value_pct_gdp", order=region_orden,
            palette="muted", ax=ax2, flierprops={"markersize": 2, "alpha": 0.4})
ax2.set_title("Distribución por región geográfica")
ax2.set_xlabel("% del PIB")
ax2.set_ylabel("")

fig.suptitle("Gasto público en educación — UNESCO UIS (1970–2025)",
                fontsize=14, fontweight="bold", y=1.01)
plt.tight_layout()
fig.savefig(figures_dir / "03_distribucion_gasto.png", bbox_inches="tight")
plt.close()
print("   ✓ 03_distribucion_gasto.png")

# 8.2 Tendencia mundial
fig, ax = plt.subplots(figsize=(13, 5))
ax.fill_between(tendencia["year"], tendencia["ic_inferior"], tendencia["ic_superior"],
                alpha=0.15, color="#2196F3", label="±1 desvío estándar")
ax.plot(tendencia["year"], tendencia["promedio_mundial"],
        color="#1565C0", lw=2, label="Promedio mundial")
ax.plot(tendencia["year"], tendencia["mediana_mundial"],
        color="#E53935", lw=1.5, linestyle="--", label="Mediana mundial")
ax2b = ax.twinx()
ax2b.bar(tendencia["year"], tendencia["n_paises"], alpha=0.12, color="gray",
            width=0.8, label="N países con dato")
ax2b.set_ylabel("N° de países", color="gray", fontsize=10)
ax2b.tick_params(axis="y", labelcolor="gray")
ax2b.set_ylim(0, tendencia["n_paises"].max() * 4)
ax.set_title("Tendencia mundial del gasto público en educación")
ax.set_xlabel("Año")
ax.set_ylabel("% del PIB")
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.1f%%"))
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2b.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=9)
plt.tight_layout()
fig.savefig(figures_dir / "03_tendencia_mundial.png", bbox_inches="tight")
plt.close()
print("   ✓ 03_tendencia_mundial.png")

# 8.3 Top / Bottom países
top10 = ranking.head(10)[["country_name", "promedio_historico", "region"]].copy()
bot10 = ranking.tail(10)[["country_name", "promedio_historico", "region"]].copy()

regiones_unicas = df["region"].unique()
palette_region = {r: c for r, c in zip(
    regiones_unicas, sns.color_palette("tab10", n_colors=len(regiones_unicas))
)}

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
for ax, data, title in [
    (axes[0], top10.sort_values("promedio_historico"), "Top 10 — Mayor gasto histórico"),
    (axes[1], bot10.sort_values("promedio_historico", ascending=False), "Bottom 10 — Menor gasto histórico"),
]:
    colors = [palette_region.get(r, "gray") for r in data["region"]]
    bars = ax.barh(data["country_name"], data["promedio_historico"],
                    color=colors, edgecolor="white", height=0.7)
    for bar, val in zip(bars, data["promedio_historico"]):
        ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
                f"{val:.2f}%", va="center", fontsize=8.5)
    ax.set_title(title)
    ax.set_xlabel("Promedio histórico (% del PIB)")
    ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.1f%%"))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

fig.suptitle("Gasto público en educación — Ranking de países (UNESCO UIS)",
                fontsize=13, fontweight="bold")
plt.tight_layout()
fig.savefig(figures_dir / "03_top_bottom_paises.png", bbox_inches="tight")
plt.close()
print("   ✓ 03_top_bottom_paises.png")

# 8.4 Cobertura temporal por región
cobertura = (
    df_base.groupby(["year", "region"])["country_code"]
    .nunique()
    .reset_index()
    .rename(columns={"country_code": "n_paises"})
)
fig, ax = plt.subplots(figsize=(13, 5))
for region, grp in cobertura.groupby("region"):
    ax.plot(grp["year"], grp["n_paises"], label=region, lw=1.5)
ax.set_title("Cobertura temporal por región geográfica")
ax.set_xlabel("Año")
ax.set_ylabel("N° de países con dato")
ax.legend(loc="upper left", fontsize=8, ncol=2)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
fig.savefig(figures_dir / "03_cobertura_temporal.png", bbox_inches="tight")
plt.close()
print("   ✓ 03_cobertura_temporal.png")

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
    figures/
        03_distribucion_gasto.png
        03_tendencia_mundial.png
        03_top_bottom_paises.png
        03_cobertura_temporal.png

Próxima etapa: Project 3 — merge con HDI dataset
""")