# 📦 Inventory Planning & Replenishment Decision Tool

Herramienta de planeación de inventarios desarrollada para apoyar la toma de decisiones de abastecimiento mediante pronóstico de demanda, cálculo de stock de seguridad, punto de reorden (ROP), análisis de riesgo de quiebre y riesgo de caducidad.

El proyecto integra técnicas de **Forecasting + Inventory Planning + Replenishment** en una aplicación interactiva desarrollada con Streamlit.

---

## 🎯 Objetivo

Desarrollar una herramienta de planeación que permita estimar la demanda de los próximos 30 días y utilizar este pronóstico para determinar políticas de inventario y acciones de abastecimiento.

El proyecto busca responder preguntas como:

- ¿Cuánta demanda se espera para los próximos 30 días?
- ¿Cuánto inventario debería mantenerse como protección ante la variabilidad de la demanda?
- ¿Cuándo debería realizarse un reabastecimiento?
- ¿Existe riesgo de quiebre antes de recibir el material?
- ¿El MOQ puede generar riesgo de caducidad?
- ¿Qué cantidad debería solicitarse?
- ¿Cómo cambia la decisión al modificar el nivel de servicio?

---

## 📊 Datos

El proyecto utiliza un conjunto de datos sintético de planeación de demanda y suministro de la industria química.

El dataset contiene información mensual a nivel SKU, incluyendo:

- Demanda real
- Inventario disponible
- Lead Time del proveedor
- Tiempo de tránsito
- MOQ (Minimum Order Quantity)
- Recepciones planificadas
- Vida útil del producto
- Prioridad del cliente
- Grupo de producto
- Unidad de medida

El conjunto de datos contiene **100 SKUs y 10 meses de información**, de noviembre de 2024 a agosto de 2025.

Para el proceso de modelado se utilizó información histórica hasta julio de 2025, utilizando agosto de 2025 como periodo de evaluación del pronóstico.

---

## 🔮 Forecasting

### Target

Se construyó un pronóstico de demanda acumulada para los siguientes 30 días:

**Forecast_30d**

El modelo trabaja con datos mensuales y genera un pronóstico de un periodo mensual, interpretado en el proyecto como la demanda esperada durante los próximos 30 días.

Para la planeación de inventarios, este valor se convierte a una demanda diaria proyectada:

# Demanda diaria proyectada = Pronóstico 30 días / 30

| Modelo                        |     MAE ↓ |     RMSE ↓ |     MAPE ↓ |       R² ↑ |
| ----------------------------- | --------: | ---------: | ---------: | ---------: |
| Forecast original Kaggle      |     89.78 |     144.79 |     23.92% |     0.8634 |
| XGBoost Base                  |     86.14 |     152.23 |     22.19% |     0.8490 |
| XGBoost + categóricas         |     82.39 |     148.16 |     21.76% |     0.8570 |
| HistGradientBoosting          |     96.93 |     168.11 |     24.56% |     0.8159 |
| Random Forest                 |     82.28 |     144.66 |     21.55% |     0.8637 |
| **Suavizamiento Exponencial** | **74.33** | **126.65** | **20.72%** | **0.8955** |
| Naive                         |     86.23 |     137.42 |     23.15% |     0.8769 |
| ARIMA(1,1,1)                  |     84.52 |     161.64 |     22.10% |     0.8298 |


# Consideración temporal del escenario

El escenario de planeación se construye utilizando julio de 2025 como periodo de decisión y agosto de 2025 como periodo objetivo del pronóstico.

Debido a que el dataset combina registros mensuales con fechas específicas de recepción, se realizó un ajuste de escenario para las fechas de recepción planificadas.

La fecha original se conserva y se genera una fecha ajustada desplazada un mes para representar la recepción dentro del periodo proyectado.

Este ajuste es exclusivamente una transformación del escenario de análisis y no una modificación de los datos originales.

# Aplicación

La herramienta fue desarrollada en Streamlit y permite:

Consultar el pronóstico de demanda de 30 días
Visualizar el desempeño del modelo
Seleccionar el nivel de servicio
Consultar el stock de seguridad
Consultar el punto de reorden
Visualizar la cobertura de inventario
Identificar riesgos de quiebre
Identificar riesgos de caducidad
Consultar cantidades recomendadas de reabastecimiento
Comparar escenarios de 90%, 95% y 98% de nivel de servicio
