"""
05_visualizacion.py — Gráficos del análisis de gasto público en educación
===========================================================================

Inputs:
    output/02_education_spending_clean.csv
    output/03_tendencia_mundial.csv
    output/03_ranking_paises.csv

Outputs:
    output/figures/03_distribucion_gasto.png
    output/figures/03_tendencia_mundial.png
    output/figures/03_top_bottom_paises.png
    output/figures/03_cobertura_temporal.png
"""

import pandas as pd
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
print("VISUALIZACIÓN — GASTO PÚBLICO EN EDUCACIÓN (UNESCO UIS)")
print("="*80)

# ============================================================================
# CARGA
# ============================================================================
print("\n📁 Cargando datasets...")
df_clean = pd.read_csv(output_dir / "02_education_spending_clean.csv")
tendencia = pd.read_csv(output_dir / "03_tendencia_mundial.csv")
ranking = pd.read_csv(output_dir / "03_ranking_paises.csv")

# Reconstruir df_base (sin NIL) con región — necesario para algunos gráficos
df_base = df_clean[~df_clean["flag_magnitude_nil"]].copy()
df_base["region"] = ranking.set_index("country_code")["region"].reindex(df_base["country_code"]).values
print(f"   ✓ df_base: {len(df_base):,} filas")
print(f"   ✓ tendencia: {len(tendencia)} años")
print(f"   ✓ ranking: {len(ranking)} países")

# ============================================================================
# 1. DISTRIBUCIÓN DEL GASTO
# ============================================================================
print("\n🎨 Generando gráficos...")

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
ax1.set_ylabel("Observaciones (Frecuencia)")
ax1.legend()

ax2 = axes[1]
region_orden = (df_base.groupby("region")["value_pct_gdp"].median()
                .sort_values().index.tolist())
sns.boxplot(data=df_base, y="region", x="value_pct_gdp", order=region_orden,
            hue="region", palette="muted", ax=ax2, legend=False,
            flierprops={"markersize": 2, "alpha": 0.4})
ax2.set_title("Distribución por región geográfica")
ax2.set_xlabel("% del PIB")
ax2.set_ylabel("")

fig.suptitle("Gasto público en educación — UNESCO UIS (1970–2025)",
                fontsize=14, fontweight="bold", y=1.01)
plt.tight_layout()
fig.savefig(figures_dir / "03_distribucion_gasto.png", bbox_inches="tight")
plt.close()
print("   ✓ 03_distribucion_gasto.png")

# ============================================================================
# 2. TENDENCIA MUNDIAL
# ============================================================================
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

# ============================================================================
# 3. TOP 10 / BOTTOM 10 PAÍSES
# ============================================================================
top10 = ranking.head(10)[["country_name", "promedio_historico", "region"]].copy()
bot10 = ranking.tail(10)[["country_name", "promedio_historico", "region"]].copy()

regiones_unicas = ranking["region"].unique()
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

# ============================================================================
# 4. COBERTURA TEMPORAL POR REGIÓN
# ============================================================================
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

print("\n" + "="*80)
print("✅ VISUALIZACIÓN COMPLETADA")
print("="*80)
print("""
Outputs generados en output/figures/:
    03_distribucion_gasto.png
    03_tendencia_mundial.png
    03_top_bottom_paises.png
    03_cobertura_temporal.png

""")