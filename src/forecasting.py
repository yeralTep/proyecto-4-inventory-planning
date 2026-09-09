import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing


def generate_forecast(input_path, output_path):
    """
    Genera un forecast de 30 días por SKU
    utilizando Suavizamiento Exponencial.
    """

    # Cargar datos
    df = pd.read_csv(input_path)

    # Convertir fecha
    df["Month"] = pd.to_datetime(df["Month"], dayfirst=True)

    # Ordenar datos
    df = df.sort_values(["SKU_ID", "Month"]).reset_index(drop=True)

    forecast_results = []

    # Generar forecast por SKU
    for sku, group in df.groupby("SKU_ID"):

        group = group.sort_values("Month")

        demand = group["Actual_Demand_units"].dropna().values

        model = ExponentialSmoothing(
            demand,
            trend=None,
            seasonal=None
        ).fit(optimized=True)

        forecast = model.forecast(1)[0]

        # Evitar valores negativos
        forecast = max(0, forecast)

        forecast_results.append({
            "SKU_ID": sku,
            "Forecast_30d": forecast
        })

    # Convertir resultados a DataFrame
    forecast_df = pd.DataFrame(forecast_results)

    # Agregar información descriptiva del SKU
    sku_info = (
        df[
            [
                "SKU_ID",
                "SKU_Description",
                "Product_Group",
                "UoM"
            ]
        ]
        .drop_duplicates("SKU_ID")
    )

    forecast_df = forecast_df.merge(
        sku_info,
        on="SKU_ID",
        how="left"
    )

    # Ordenar columnas
    forecast_df = forecast_df[
        [
            "SKU_ID",
            "SKU_Description",
            "Product_Group",
            "UoM",
            "Forecast_30d"
        ]
    ]

    # Guardar resultado
    forecast_df.to_csv(output_path, index=False)

    return forecast_df

