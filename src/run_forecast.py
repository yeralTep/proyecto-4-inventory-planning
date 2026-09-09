from forecasting import generate_forecast


input_path = "data/Demand_Supply_Planning_train.csv"
output_path = "outputs/forecast_30d.csv"


forecast_df = generate_forecast(
    input_path=input_path,
    output_path=output_path
)

print("Forecast generado correctamente.")
print(f"SKUs procesados: {len(forecast_df)}")
print(f"Archivo guardado en: {output_path}")