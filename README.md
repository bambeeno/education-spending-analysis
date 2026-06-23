# Education Spending Analysis

Análisis del gasto público en educación a nivel global (% del PBI), usando datos
de UNESCO Institute for Statistics (UIS) — indicador `XGDP.FSGOV`, equivalente al
`SE.XPD.TOTL.GD.ZS` del Banco Mundial.

Segundo proyecto de un portfolio de Data Engineering, en continuidad con
[human-development-analysis](https://github.com/bambeeno/human-development-analysis)
(Proyecto 1 — HDI).

## Stack
Python · Pandas · Matplotlib · Git

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
├── output/         # CSVs procesados (no versionados salvo entregables)
├── docs/           # Notas de contexto histórico sobre casos especiales del dataset
└── README.md
```

## Estado del pipeline

| Script | Descripción | Estado |
|---|---|---|
| `01_exploracion.py` | Filtrado del indicador, inspección de cobertura, outliers, nulos | ✅ Hecho |
| `02_limpieza.py` | Normalización a snake_case, flags explícitos (sin eliminar/imputar) | ✅ Hecho |
| `03_analisis.py` | Análisis por región, evolución histórica, caída pandémica | ⬜ Pendiente |
| `04_exportar.py` | Exportación a Excel con resumen ejecutivo | ⬜ Pendiente |
| `05_visualizacion.py` | Gráficos | ⬜ Pendiente |

**Dataset resultante:** 5,159 registros · 206 países · 1970–2025 · sin nulos en
`VALUE`.

## Principio de limpieza: nada se elimina sin documentar por qué

Esta es la decisión metodológica central del proyecto: ningún outlier o hueco se
descarta o imputa sin antes investigar si tiene una explicación de contexto real
(crisis política, particularidad económica, limitación del indicador). El detalle
completo, con fuentes, está en [`docs/notas_contextuales.md`](docs/notas_contextuales.md).

Casos documentados hasta ahora:
- **Türkiye, 1998** — dato marcado `NIL` por la fuente, coincidente con un año de
  fuerte crisis institucional (crisis diplomática con Siria por el caso Öcalan,
  ilegalización del partido islamista Refah, gobiernos de coalición inestables).
- **Micronesia y otros microestados insulares del Pacífico** (Kiribati, Tuvalu,
  Marshall Islands, Nauru, entre otros) — valores extremos explicados por
  financiamiento externo (fondos de fideicomiso de EE.UU.) dividido sobre un PBI
  local mínimo, no por errores de medición.
- **Pendientes de investigar**: Cuba (gasto alto y sostenido 2005–2020) y un
  posible patrón regional en Lesotho, Botswana y Namibia.

## Próximos pasos
- Análisis exploratorio por región y por década
- Investigar el "efecto pandemia" en el gasto educativo global (caída del 4.16%
  en 2019 al 3.51% en 2023, según fuentes externas) — posible gancho narrativo
  compartido con el Proyecto 1 (HDI)
- Proyecto 3: cruce de este dataset con HDI para análisis de correlación
