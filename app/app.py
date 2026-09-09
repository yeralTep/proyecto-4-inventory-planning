import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Inventory Planning",
    page_icon="🧪",
    layout="wide"
)


# ============================================================
# ESTILO VISUAL
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #F8F6FC;
    }

    .main-title {
        color: #4B1F6F;
        font-size: 38px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .subtitle {
        color: #6B5B73;
        font-size: 17px;
        margin-top: 0px;
        margin-bottom: 25px;
    }

    .section-title {
        color: #4B1F6F;
        font-size: 27px;
        font-weight: 650;
        margin-top: 25px;
        margin-bottom: 8px;
    }

    .section-description {
        color: #6B5B73;
        font-size: 15px;
        margin-bottom: 18px;
    }

    .metric-card {
        background-color: white;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #E5DDF0;
        text-align: center;
    }

    .metric-label {
        color: #7B6B84;
        font-size: 14px;
    }

    .metric-value {
        color: #4B1F6F;
        font-size: 25px;
        font-weight: 700;
    }

    .info-box {
        background-color: #F0EAF7;
        padding: 16px 20px;
        border-radius: 10px;
        border-left: 4px solid #7B4BA3;
        color: #4B3B52;
        margin-top: 10px;
        margin-bottom: 20px;
    }

    hr {
        border-color: #E5DDF0;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# RUTAS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = BASE_DIR / "outputs"


# ============================================================
# CARGAR DATOS
# ============================================================

forecast_path = OUTPUTS_DIR / "forecast_30d.csv"

forecast = pd.read_csv(forecast_path)

forecast["Forecast_30d"] = pd.to_numeric(
    forecast["Forecast_30d"],
    errors="coerce"
)


# ============================================================
# DATOS DE VALIDACIÓN
# ============================================================

original_path = BASE_DIR / "data" / "Demand Supply Planning.csv"

df_original = pd.read_csv(original_path)

df_original["Month"] = pd.to_datetime(
    df_original["Month"],
    dayfirst=True
)


actual_august = df_original[
    df_original["Month"] == pd.Timestamp("2025-08-01")
][
    ["SKU_ID", "Actual_Demand_units"]
].copy()


# Unir forecast con demanda real de agosto
validation = forecast.merge(
    actual_august,
    on="SKU_ID",
    how="left"
)


# ============================================================
# TÍTULO
# ============================================================

st.markdown(
    '<div class="main-title">🧪 Inventory Planning</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Chemical Supply Chain · Planeación de inventarios basada en pronóstico de demanda'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SECCIÓN 1 — FORECASTING
# ============================================================

st.markdown(
    '<div class="section-title">1. Forecasting</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Pronóstico de demanda a 30 días generado mediante Suavizamiento Exponencial.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# RESUMEN DEL MODELO
# ============================================================

col1, col2, col3 = st.columns([1.2, 1.8, 1.8])


# ============================================================
# MODELO SELECCIONADO
# ============================================================

with col1:

    st.markdown(
        """
        <div class="info-box">
        <strong>Modelo seleccionado</strong>
        <br><br>
        Suavizamiento Exponencial
        <br><br>
        Mejor desempeño general entre los modelos evaluados.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DESEMPEÑO DEL MODELO
# ============================================================

with col2:

    st.markdown("**Desempeño del modelo**")

    metricas = pd.DataFrame({
        "Métrica": [
            "MAE",
            "RMSE",
            "MAPE",
            "R²"
        ],
        "Resultado": [
            "74.33",
            "126.65",
            "20.72%",
            "0.8955"
        ]
    })

    st.dataframe(
        metricas,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# SIGNIFICADO DE LAS MÉTRICAS
# ============================================================

with col3:

    st.markdown("**¿Qué significa cada métrica?**")

    st.markdown(
        """
        **MAE:** error promedio del pronóstico en unidades.

        **RMSE:** penaliza más los errores grandes.

        **MAPE:** error promedio expresado como porcentaje.

        **R²:** proporción de la variabilidad explicada por el modelo.
        """
    )


# ============================================================
# VALIDACIÓN — AGOSTO 2025
# ============================================================

st.subheader("Validación del pronóstico — Agosto 2025")

st.markdown(
    """
    El pronóstico de 30 días se generó utilizando la información disponible
    hasta julio de 2025. La demanda real de agosto se utiliza únicamente
    como periodo de validación.
    """
)

# ============================================================
# GRÁFICA FORECAST VS DEMANDA REAL
# ============================================================

st.markdown("**Pronóstico 30 días vs demanda real de agosto 2025**")

line_chart_data = validation[
    [
        "SKU_ID",
        "Forecast_30d",
        "Actual_Demand_units"
    ]
].copy()

line_chart_data = line_chart_data.sort_values("SKU_ID")

line_chart_data = line_chart_data.set_index("SKU_ID")

line_chart_data = line_chart_data.rename(
    columns={
        "Forecast_30d": "Pronóstico 30 días",
        "Actual_Demand_units": "Demanda real agosto"
    }
)

st.line_chart(
    line_chart_data,
    use_container_width=True
)
# ============================================================
# SELECTOR DE SKU
# ============================================================

st.subheader("Consulta por SKU")

sku_selected = st.selectbox(
    "Selecciona un SKU",
    options=forecast["SKU_ID"].tolist()
)


sku_data = validation[
    validation["SKU_ID"] == sku_selected
].iloc[0]


# ============================================================
# DETALLE DEL SKU
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Pronóstico 30 días</div>
            <div class="metric-value">
                {sku_data["Forecast_30d"]:,.0f}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Demanda real agosto</div>
            <div class="metric-value">
                {sku_data["Actual_Demand_units"]:,.0f}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    error = (
        sku_data["Forecast_30d"]
        - sku_data["Actual_Demand_units"]
    )

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Error del pronóstico</div>
            <div class="metric-value">
                {error:,.0f}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# TABLA DE DETALLE
# ============================================================

st.markdown("**Detalle del pronóstico seleccionado**")

detalle = pd.DataFrame({
    "SKU": [sku_data["SKU_ID"]],
    "Descripción": [sku_data["SKU_Description"]],
    "Grupo": [sku_data["Product_Group"]],
    "Unidad": [sku_data["UoM"]],
    "Pronóstico 30 días": [sku_data["Forecast_30d"]],
    "Demanda real agosto": [sku_data["Actual_Demand_units"]]
})

st.dataframe(
    detalle,
    use_container_width=True,
    hide_index=True
)

# ============================================================
# NIVEL DE SERVICIO
# ============================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">2. Nivel de servicio</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Selecciona el nivel de protección que se utilizará para la planeación del inventario.'
    '</div>',
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


# ============================================================
# SELECTOR
# ============================================================

with col1:

    st.markdown("**Selecciona el nivel de servicio**")

    nivel_servicio = st.selectbox(
        "Nivel de servicio",
        options=[90, 95, 98],
        index=1,
        format_func=lambda x: f"{x}%",
        label_visibility="collapsed"
    )

    st.markdown(
        f"""
        <div class="info-box">
        <strong>Escenario seleccionado: {nivel_servicio}%</strong>
        <br><br>
        Este nivel determina el Stock de Seguridad y el Punto de Reorden
        utilizados en la planeación.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# EXPLICACIÓN DE LOS NIVELES
# ============================================================

with col2:

    st.markdown("**¿Qué significa cada nivel de servicio?**")

    niveles = pd.DataFrame({
        "Nivel": [
            "90%",
            "95%",
            "98%"
        ],
        "Interpretación": [
            "Menor protección ante la variabilidad y mayor riesgo de quiebre.",
            "Escenario base / estándar de protección.",
            "Mayor protección ante la variabilidad y menor riesgo de quiebre, a costa de mayor inventario."
        ]
    })

    st.dataframe(
        niveles,
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# CARGA DEL ESCENARIO SELECCIONADO
# ============================================================

archivo_plan = OUTPUTS_DIR / (
    f"plan_inventarios_{nivel_servicio}.csv"
)

plan = pd.read_csv(archivo_plan)


st.success(
    f"Escenario de {nivel_servicio}% seleccionado · "
    f"{len(plan)} SKUs disponibles para la planeación."
)

# ============================================================
# SECCIÓN 3 — PLANEACIÓN DE INVENTARIOS
# ============================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">3. Planeación de inventarios</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Evaluación de la posición actual de inventario y de los niveles '
    'de protección requeridos según el nivel de servicio seleccionado.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# KPIs GENERALES
# ============================================================

total_skus = len(plan)

skus_reabastecer = (
    plan["Accion_Final"]
    .isin([
        "Reabastecer",
        "Reabastecer - Negociar MOQ",
        "Urgente - Riesgo de quiebre"
    ])
    .sum()
)

skus_quiebre = (
    plan["Accion_Final"]
    == "Urgente - Riesgo de quiebre"
).sum()

skus_ok = (
    plan["Accion_Final"]
    == "OK"
).sum()


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "SKUs analizados",
        f"{total_skus}"
    )

with col2:
    st.metric(
        "Requieren reabastecimiento",
        f"{skus_reabastecer}"
    )

with col3:
    st.metric(
        "Riesgo de quiebre",
        f"{skus_quiebre}"
    )

with col4:
    st.metric(
        "OK",
        f"{skus_ok}"
    )


# ============================================================
# NIVEL DE SERVICIO SELECCIONADO
# ============================================================

st.subheader(
    f"Escenario de nivel de servicio: {nivel_servicio}%"
)

st.markdown(
    f"""
    <div class="info-box">
    El escenario seleccionado utiliza un nivel de servicio de
    <strong>{nivel_servicio}%</strong>. Los valores de stock de seguridad
    y punto de reorden corresponden a este escenario.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TABLA DE PLANEACIÓN
# ============================================================

st.subheader("Posición de inventario por SKU")

tabla_inventario = plan[
    [
        "ID_SKU",
        "Descripcion_SKU",
        "Demanda_Diaria_Proyectada",
        "Inventario_Actual",
        "Dias_Inventario_Proyectados",
        "LeadTime_Total_dias",
        "Demanda_Durante_LeadTime",
        "Stock_Seguridad",
        "Punto_Reorden"
    ]
].copy()


tabla_inventario = tabla_inventario.rename(
    columns={
        "ID_SKU": "SKU",
        "Descripcion_SKU": "Descripción",
        "Demanda_Diaria_Proyectada": "Demanda diaria",
        "Inventario_Actual": "Inventario actual",
        "Dias_Inventario_Proyectados": "Días de inventario",
        "LeadTime_Total_dias": "Lead Time total",
        "Demanda_Durante_LeadTime": "Demanda durante LT",
        "Stock_Seguridad": "Stock de seguridad",
        "Punto_Reorden": "ROP"
    }
)


st.dataframe(
    tabla_inventario,
    use_container_width=True,
    hide_index=True,
    column_config={
        "SKU": st.column_config.TextColumn(
            "SKU",
            width="small"
        ),
        "Descripción": st.column_config.TextColumn(
            "Descripción",
            width="medium"
        ),
        "Demanda diaria": st.column_config.NumberColumn(
            "Demanda diaria",
            format="%.1f"
        ),
        "Inventario actual": st.column_config.NumberColumn(
            "Inventario actual",
            format="%.0f"
        ),
        "Días de inventario": st.column_config.NumberColumn(
            "Días de inventario",
            format="%.1f días"
        ),
        "Lead Time total": st.column_config.NumberColumn(
            "Lead Time total",
            format="%.0f días"
        ),
        "Demanda durante LT": st.column_config.NumberColumn(
            "Demanda durante LT",
            format="%.0f"
        ),
        "Stock de seguridad": st.column_config.NumberColumn(
            "Stock de seguridad",
            format="%.0f"
        ),
        "ROP": st.column_config.NumberColumn(
            "ROP",
            format="%.0f"
        )
    }
)

# ============================================================
# SECCIÓN 4 — ABASTECIMIENTO Y RIESGOS
# ============================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">4. Abastecimiento y riesgos</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Evaluación del inventario considerando las recepciones planificadas, '
    'el MOQ y la vida útil del producto para determinar los principales '
    'riesgos y la acción recomendada.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# KPIs DE RIESGO
# ============================================================

total_skus = len(plan)

riesgo_quiebre = (
    plan["Riesgo_Quiebre_Antes_Recepcion"] == "Alto"
).sum()

riesgo_caducidad_inventario = (
    plan["Riesgo_Caducidad_Inventario"] == "Alto"
).sum()

riesgo_caducidad_moq = (
    plan["Riesgo_Caducidad_MOQ"]
    == "Negociar MOQ - Alto riesgo de caducar"
).sum()

negociar_moq = (
    plan["Accion_Final"]
    == "Reabastecer - Negociar MOQ"
).sum()


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "SKUs analizados",
        f"{total_skus}"
    )

with col2:
    st.metric(
        "Riesgo de quiebre",
        f"{riesgo_quiebre}"
    )

with col3:
    st.metric(
        "Riesgo de caducidad por MOQ",
        f"{riesgo_caducidad_moq}"
    )

with col4:
    st.metric(
        "Negociar MOQ",
        f"{negociar_moq}"
    )


# ============================================================
# EXPLICACIÓN DEL SEMÁFORO
# ============================================================

st.subheader("Semáforo de decisión")

semaforo = pd.DataFrame({
    "Semáforo": [
        "🟢 OK",
        "🟠 Reabastecer",
        "🔴 Reabastecer - Negociar MOQ",
        "🔴 Urgente - Riesgo de quiebre"
    ],
    "Significado": [
        "El inventario proyectado es suficiente respecto al nivel de protección requerido.",
        "El inventario proyectado se encuentra por debajo del punto de reorden.",
        "Se requiere reabastecimiento, pero el MOQ puede generar riesgo de caducidad.",
        "El inventario actual puede agotarse antes de la recepción planificada."
    ]
})

st.dataframe(
    semaforo,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# FILTROS
# ============================================================

st.subheader("Evaluación de abastecimiento")

filtro1, filtro2 = st.columns(2)

with filtro1:

    filtro_accion = st.multiselect(
        "Acción",
        options=[
            "OK",
            "Reabastecer",
            "Reabastecer - Negociar MOQ",
            "Urgente - Riesgo de quiebre"
        ],
        placeholder="Todas"
    )

with filtro2:

    filtro_quiebre = st.multiselect(
        "Riesgo de quiebre",
        options=sorted(
            plan["Riesgo_Quiebre_Antes_Recepcion"]
            .dropna()
            .unique()
            .tolist()
        ),
        placeholder="Todos"
    )


# ============================================================
# APLICAR FILTROS
# ============================================================

plan_riesgos = plan.copy()


if filtro_accion:

    plan_riesgos = plan_riesgos[
        plan_riesgos["Accion_Final"].isin(filtro_accion)
    ]


if filtro_quiebre:

    plan_riesgos = plan_riesgos[
        plan_riesgos["Riesgo_Quiebre_Antes_Recepcion"].isin(
            filtro_quiebre
        )
    ]


# ============================================================
# CREAR SEMÁFORO
# ============================================================

def obtener_semaforo_riesgo(accion):

    if accion == "OK":
        return "🟢"

    elif accion == "Reabastecer":
        return "🟠"

    elif accion == "Reabastecer - Negociar MOQ":
        return "🔴"

    elif accion == "Urgente - Riesgo de quiebre":
        return "🔴"

    return "⚪"


plan_riesgos["Semáforo"] = (
    plan_riesgos["Accion_Final"]
    .apply(obtener_semaforo_riesgo)
)


# ============================================================
# TABLA DE ABASTECIMIENTO Y RIESGOS
# ============================================================

st.markdown(
    f"**{len(plan_riesgos)} SKUs mostrados**"
)


tabla_riesgos = plan_riesgos[
    [
        "Semáforo",
        "ID_SKU",
        "Descripcion_SKU",
        "Inventario_Actual",
        "Inventario_Despues_Recepcion",
        "Cobertura_MOQ_dias",
        "MOQ",
        "Vida_Util_dias",
        "Riesgo_Quiebre_Antes_Recepcion",
        "Riesgo_Caducidad_Inventario",
        "Riesgo_Caducidad_MOQ",
        "Cantidad_Recomendada",
        "Accion_Final"
    ]
].copy()


# ============================================================
# DÍAS DE INVENTARIO DESPUÉS DE RECEPCIÓN
# ============================================================

tabla_riesgos["Dias_Inventario_Despues_Recepcion"] = (
    plan_riesgos["Inventario_Despues_Recepcion"]
    / plan_riesgos["Demanda_Diaria_Proyectada"]
)


# Reordenar columnas
tabla_riesgos = tabla_riesgos[
    [
        "Semáforo",
        "ID_SKU",
        "Descripcion_SKU",
        "Inventario_Actual",
        "Inventario_Despues_Recepcion",
        "Dias_Inventario_Despues_Recepcion",
        "MOQ",
        "Vida_Util_dias",
        "Cobertura_MOQ_dias",
        "Riesgo_Quiebre_Antes_Recepcion",
        "Riesgo_Caducidad_Inventario",
        "Riesgo_Caducidad_MOQ",
        "Cantidad_Recomendada",
        "Accion_Final"
    ]
]


# ============================================================
# RENOMBRAR COLUMNAS
# ============================================================

tabla_riesgos = tabla_riesgos.rename(
    columns={
        "ID_SKU": "SKU",
        "Descripcion_SKU": "Descripción",
        "Inventario_Actual": "Inventario actual",
        "Inventario_Despues_Recepcion": "Inventario después recepción",
        "Dias_Inventario_Despues_Recepcion": "Días inventario después recepción",
        "MOQ": "MOQ",
        "Vida_Util_dias": "Vida útil",
        "Cobertura_MOQ_dias": "Cobertura MOQ",
        "Riesgo_Quiebre_Antes_Recepcion": "Riesgo quiebre",
        "Riesgo_Caducidad_Inventario": "Riesgo caducidad inventario",
        "Riesgo_Caducidad_MOQ": "Riesgo caducidad MOQ",
        "Cantidad_Recomendada": "Cantidad recomendada",
        "Accion_Final": "Acción final"
    }
)


# ============================================================
# MOSTRAR TABLA
# ============================================================

st.dataframe(
    tabla_riesgos,
    use_container_width=True,
    hide_index=True,
    column_config={

        "Semáforo": st.column_config.TextColumn(
            "Estado",
            width="small"
        ),

        "SKU": st.column_config.TextColumn(
            "SKU",
            width="small"
        ),

        "Descripción": st.column_config.TextColumn(
            "Descripción",
            width="medium"
        ),

        "Inventario actual": st.column_config.NumberColumn(
            "Inventario actual",
            format="%.0f",
            width="small"
        ),

        "Inventario después recepción": st.column_config.NumberColumn(
            "Inventario post-recepción",
            format="%.0f",
            width="medium"
        ),

        "Días inventario después recepción": st.column_config.NumberColumn(
            "Días inventario post-recepción",
            format="%.1f",
            width="medium"
        ),

        "MOQ": st.column_config.NumberColumn(
            "MOQ",
            format="%.0f",
            width="small"
        ),

        "Vida útil": st.column_config.NumberColumn(
            "Vida útil",
            format="%.0f días",
            width="small"
        ),

        "Cobertura MOQ": st.column_config.NumberColumn(
            "Cobertura MOQ",
            format="%.1f días",
            width="small"
        ),

        "Riesgo quiebre": st.column_config.TextColumn(
            "Riesgo quiebre",
            width="small"
        ),

        "Riesgo caducidad inventario": st.column_config.TextColumn(
            "Riesgo caducidad",
            width="small"
        ),

        "Riesgo caducidad MOQ": st.column_config.TextColumn(
            "Riesgo MOQ",
            width="small"
        ),

        "Cantidad recomendada": st.column_config.NumberColumn(
            "Cantidad a pedir",
            format="%.0f",
            width="small"
        ),

        "Acción final": st.column_config.TextColumn(
            "Acción",
            width="medium"
        )
    }
)
