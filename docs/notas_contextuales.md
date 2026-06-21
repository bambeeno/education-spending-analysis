# Notas contextuales — Education Spending Analysis

Este documento registra casos donde un dato "raro" en el dataset (outlier, hueco,
valor especial) tiene una explicación de contexto real — político, económico o social —
que vale la pena conocer antes de decidir cómo tratarlo en la limpieza o el análisis.

La idea: un dataset de desarrollo humano no son números aislados. Los huecos y
anomalías muchas veces *son* el dato — reflejan crisis, rupturas institucionales,
o cambios de prioridad de un país en un momento dado. Documentar el porqué evita
tratarlos como ruido a descartar sin criterio.

---

## Türkiye, 1998 — MAGNITUDE = NIL

**El dato:** En el dataset UNESCO UIS (`SDG_DATA_NATIONAL.csv`), el registro de
Turquía para el indicador `XGDP.FSGOV` (gasto público en educación, % del PBI) en
1998 tiene `VALUE = 0.0` con `MAGNITUDE = NIL`.

Según el README oficial de UNESCO UIS:
> **NIL** – The value will be 0, and should be treated as NIL.

Es decir, no es un dato faltante (`NaN`) ni un valor real de 0% de gasto — es un
código que indica que el dato no se registró de forma válida ese año.

**Por qué pasó (contexto histórico):**

1998 fue un año de fuerte inestabilidad institucional y de seguridad en Turquía:

- **Crisis diplomática con Siria por el caso Öcalan:** Turquía escaló la presión
  militar sobre Siria (que albergaba a Abdullah Öcalan, líder del PKK), con
  movilización de tropas en la frontera. La crisis se resolvió recién a fines de
  año con la expulsión de Öcalan y el Acuerdo de Adana.
- **Purga institucional del islamismo político:** tras el "golpe posmoderno" militar
  de 1997 que forzó la renuncia del primer ministro islamista Necmettin Erbakan,
  en 1998 el Tribunal Constitucional ilegalizó su partido (Refah) y lo inhabilitó
  para ejercer cargos públicos.
- **Gobiernos de coalición débiles:** bajo Mesut Yılmaz, los gobiernos enfrentaron
  mociones de censura recurrentes, denuncias de corrupción, y poca capacidad de
  sostener reformas o procesos administrativos de largo plazo.

**Hipótesis de trabajo:** un Estado con el aparato de gobierno concentrado en una
crisis de seguridad nacional y una purga política simultánea es un entorno propenso
a que reportes estadísticos sectoriales (como el de gasto educativo) no se consoliden
o no se envíen en tiempo y forma a organismos internacionales como UNESCO. El `NIL`
de 1998 probablemente sea un artefacto administrativo/político de ese momento, no
un reflejo de que Turquía gastó efectivamente cero en educación.

**Fuentes:**
- [Crisis diplomática entre Siria y Turquía de 1998 — Wikipedia](https://es.wikipedia.org/wiki/Crisis_diplom%C3%A1tica_entre_Siria_y_Turqu%C3%ADa_de_1998)
- [Memorándum militar turco de 1997 — Wikipedia](https://es.wikipedia.org/wiki/Memor%C3%A1ndum_militar_turco_de_1997)
- [1998 Country Report on Human Rights Practices: Turkey — US Department of State](https://1997-2001.state.gov/global/human_rights/1998_hrp_report/turkey.html)

**Decisión tomada:** no se elimina ni se imputa el valor en la etapa de limpieza.
Se conserva la fila tal cual viene de la fuente, con un flag explícito
(`magnitude_flag` o equivalente) para que sea visible y excluible de forma
consciente en la etapa de análisis si hace falta (ej. al calcular promedios o
series temporales de Turquía).

---

## Micronesia (Federated States of), 1972 — outlier (66.90% del PBI)

**El dato:** valor de gasto público en educación de 66.90% del PBI en 1972, muy por
encima de la media global (~4.3%) y del resto de la serie histórica de cualquier
país en el dataset. Micronesia vuelve a aparecer 8 veces más en el listado de
outliers (umbral >3 desvíos estándar, 10.56%) entre 2012 y 2020.

**Por qué pasó (contexto histórico y mecanismo estadístico):**

En 1972, las futuras Islas Federadas de Micronesia todavía formaban parte del
**Territorio en Fideicomiso de las Islas del Pacífico (TTPI)**, administrado por
Estados Unidos — no eran un país soberano con economía propia. Ese mismo año fue,
además, un punto de quiebre político: EE.UU. abrió negociaciones separadas con las
Islas Marianas del Norte, lo que inició el proceso de fragmentación del fideicomiso
(Palaos e Islas Marshall siguieron caminos políticos propios poco después).

El pico del 66.90% combina varios factores, no uno solo:

1. **Inyección masiva de fondos externos de EE.UU.**: durante esa década, Washington
   incrementó fuertemente las subvenciones al territorio, gran parte destinada a
   construir infraestructura escolar y capacitar maestros, como preparación para la
   futura transición política.
2. **PBI local minúsculo**: en 1972 Micronesia tenía una economía de subsistencia,
   sin producción industrial ni comercial significativa. Cualquier presupuesto
   externo, al dividirse sobre un PBI casi inexistente, da un porcentaje
   matemáticamente desproporcionado.
3. **Distorsión metodológica de la fuente**: organismos como el Banco Mundial o
   UNESCO computan ese gasto como "gasto público local", aunque el dinero viniera
   de los contribuyentes de EE.UU. — el indicador no distingue origen del
   financiamiento (consistente con la limitación ya anotada sobre gasto público
   vs. privado/externo).
4. **Dispersión geográfica**: la población distribuida en cientos de islas pequeñas
   obligaba a construir escuelas repetidas por distrito en lugar de centralizar,
   elevando costos logísticos por habitante.

**Confirmación de la hipótesis "se normaliza con el tiempo":** para 2020, el gasto
de Micronesia se estabilizó en 11.56% del PBI — todavía alto respecto al promedio
mundial (~4.5%), pero ya sin la distorsión extrema de 1972. Refleja la maduración
de una economía local real, ya no dependiente casi exclusivamente de fondos
externos de fideicomiso.

**Fuentes:**
- [Federated States of Micronesia — Forum of Federations](https://forumfedorg.b-cdn.net/libdocs/FedCountries/FC-Micronesia.pdf)
- [Federated States of Micronesia — Wikipedia (EN)](https://en.wikipedia.org/wiki/Federated_States_of_Micronesia)
- [Micronesia — Education spending — The Global Economy](https://www.theglobaleconomy.com/Micronesia/Education_spending/)
- [World Bank metadata glossary — SE.XPD.TOTL.GD.ZS](https://databank.worldbank.org/metadataglossary/world-development-indicators/series/SE.XPD.TOTL.GD.ZS)

**Decisión tomada:** se conserva el dato sin alterar. Se confirma como caso
explicado (no error), y queda como evidencia de la limitación estructural del
indicador en microestados con historia colonial/de fideicomiso reciente.

---

## Patrón general — microestados insulares del Pacífico

Al revisar el conjunto completo de outliers (>3 desvíos estándar, umbral 10.56%
del PBI) en `02_education_spending_clean.csv`, 9 de los 14 países involucrados son
microestados insulares con perfiles económicos similares a Micronesia: **Kiribati**
(13 registros), **Micronesia** (9), **Tuvalu** (4), **Marshall Islands** (4),
**Nauru** (1), **American Samoa** (1), **Vanuatu** (1) — todos con PBI nominal muy
bajo y, en varios casos, historia de fideicomiso o asociación estrecha con
potencias administradoras (EE.UU., en varios de estos casos).

**Hipótesis de trabajo (a confirmar caso por caso si hace falta para el análisis):**
el mismo mecanismo que explica Micronesia 1972 — financiamiento externo
desproporcionado dividido sobre un PBI local minúsculo — probablemente explica la
mayoría de estos registros, no errores de carga de datos.

**Decisión tomada:** no se excluyen estos países del dataset. Quedan marcados con
`flag_outlier_3std = True` en la limpieza, visibles y filtrables explícitamente en
el análisis si se decide tratarlos como grupo aparte (ej. excluir microestados de
correlaciones globales, o analizarlos como categoría propia).

---

## Pendientes de investigar

Los siguientes casos aparecen repetidamente en los outliers pero todavía no tienen
contexto documentado — quedan marcados con flag en el dataset, sin alterar, hasta
investigarlos:

- **Cuba** (8 apariciones, 2005-2020, consistentemente 10.5-14% del PBI): a
  diferencia de los microestados, es una economía grande y diversificada — no
  aplica la misma explicación de "PBI minúsculo". Es de público conocimiento que
  Cuba declara la educación prioridad de Estado, lo que es coherente con un gasto
  alto y *sostenido* (no un pico aislado), pero falta confirmar con fuente.
- **Lesotho, Botswana, Namibia** (sur de África, varias apariciones cada uno):
  posible patrón regional a investigar — podría relacionarse con políticas
  post-apartheid de inversión educativa en la región, pero es una hipótesis sin
  confirmar todavía.