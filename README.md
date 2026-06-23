# Education Spending Analysis

Análisis del gasto público en educación a nivel global (% del PBI), usando datos
de UNESCO Institute for Statistics (UIS) — indicador `XGDP.FSGOV`, equivalente al
`SE.XPD.TOTL.GD.ZS` del Banco Mundial.

Segundo proyecto de un portfolio de Data Engineering, en continuidad con
[human-development-analysis](https://github.com/bambeeno/human-development-analysis)
(Proyecto 1 — HDI).

## Stack
Python · Pandas · Matplotlib · Seaborn · openpyxl · Git

## Dataset
UNESCO UIS Bulk Download — paquete "SDG 4 Education - Global and Thematic
Indicators" (última actualización: febrero 2026).
Fuente: https://databrowser.uis.unesco.org/resources/bulk

Indicador filtrado: `XGDP.FSGOV` — Government expenditure on education as a
percentage of GDP (%).

**Por qué UNESCO UIS y no el CSV directo del Banco Mundial:** el export de
`data.worldbank.org` para este indicador venía truncado en 2016 por un problema
del lado del export/cache, no de los datos reales. UNESCO UIS es además la fuente
primaria de la que el Banco Mundial re-empaqueta este indicador.

## Estructura
```
education-spending-analysis/
├── data/           # CSVs crudos de UNESCO UIS (no versionados)
├── notebooks/      # Scripts por etapa
├── output/         # CSVs procesados y entregables (infografía, Excel)
├── docs/           # Notas de contexto histórico sobre casos especiales del dataset
└── README.md
```

## Pipeline

| Script | Descripción | Estado |
|---|---|---|
| `01_exploracion.py` | Filtrado del indicador, inspección de cobertura, outliers, nulos | ✅ Hecho |
| `02_limpieza.py` | Normalización a snake_case, flags explícitos (sin eliminar/imputar) | ✅ Hecho |
| `03_analisis.py` | Estadísticas descriptivas, tendencia mundial, ranking de países | ✅ Hecho |
| `04_exportar.py` | Excel con 6 hojas: stats, tendencia, ranking, región, casos especiales, metadatos | ✅ Hecho |
| `05_visualizacion.py` | 4 gráficos PNG: distribución, tendencia mundial, ranking, cobertura temporal | ✅ Hecho |

**Dataset resultante:** 5,158 registros · 206 países · 1970–2025 · sin nulos en `VALUE`.

## Hallazgos principales

- **Mediana mundial:** 4.14% del PIB — de cada 100 dólares que produce una economía, apenas 4 van a educación.
- **Distribución muy sesgada:** la mayoría de países se concentra entre 2% y 6%, pero la cola derecha revela casos extremos con explicación histórica propia.
- **Cobertura cayó a fines de los 90s:** no porque los países gastaran menos, sino porque dejaron de reportar — crisis financiera asiática, ajustes del FMI, reformas internas de UNESCO UIS.
- **Los extremos no siempre significan lo mismo:** los microestados del Pacífico dominan el top del ranking por financiamiento externo dividido sobre PIB mínimo. Mónaco aparece en el bottom por el efecto inverso: PIB per cápita tan alto que cualquier gasto luce pequeño en porcentaje.

## Principio de limpieza: nada se elimina sin documentar por qué

Esta es la decisión metodológica central del proyecto: ningún outlier o hueco se
descarta o imputa sin antes investigar si tiene una explicación de contexto real
(crisis política, particularidad económica, limitación del indicador). El detalle
completo, con fuentes, está en [`docs/notas_contextuales.md`](docs/notas_contextuales.md).

Casos documentados:
- **Türkiye, 1998** — dato marcado `NIL` por la fuente, coincidente con un año de fuerte crisis institucional (crisis diplomática con Siria, ilegalización del partido Refah, gobiernos de coalición inestables).
- **Micronesia y otros microestados del Pacífico** (Kiribati, Tuvalu, Marshall Islands, Nauru) — valores extremos por financiamiento externo de EE.UU. dividido sobre PIB de subsistencia. No son errores de medición.
- **Mónaco** — gasto aparentemente bajo por PIB per cápita extremadamente alto. Caso límite del indicador.
- **Caída de cobertura 1995–2002** — artefacto de crisis institucional global, no reducción real del gasto.
- **Pendientes de investigar:** Cuba (gasto alto y sostenido 2005–2020) y posible patrón regional en Lesotho, Botswana y Namibia.

## Infografía

![56 años de gasto público en educación global](output/56_años_de_gasto_público_en_educación_global.png)

## Continuación del portfolio

- **Project 3:** Impacto de la pandemia en el gasto educativo global (2018–2025)
- **Project 4:** Correlación HDI × gasto educativo — cruce con el dataset del Proyecto 1