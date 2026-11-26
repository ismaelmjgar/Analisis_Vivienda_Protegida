from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# Se utiliza el CSV completo que ya forma parte del proyecto.
directorio = Path(__file__).resolve().parent
datos = pd.read_csv(directorio / "viviendas.csv", encoding="utf-8-sig")

if datos.empty or datos[["ccaa", "year", "value"]].isna().any().any():
    raise ValueError("Revisa los datos de comunidad, año y número de viviendas.")

datos["value"] = pd.to_numeric(datos["value"], errors="raise")
datos["year"] = pd.to_numeric(datos["year"], errors="raise")

if (datos["value"] < 0).any():
    raise ValueError("El número de viviendas debe ser mayor o igual que cero.")

# Cada fila puede representar varias viviendas. Se suman sus valores.
resumen = datos.groupby("ccaa", as_index=False).agg(
    registros=("value", "size"),
    viviendas=("value", "sum"),
    media_por_registro=("value", "mean"),
    minimo_por_registro=("value", "min"),
    maximo_por_registro=("value", "max"),
    primer_anio=("year", "min"),
    ultimo_anio=("year", "max"),
)
resumen = resumen.sort_values("viviendas", ascending=False)
total_viviendas = resumen["viviendas"].sum()

if total_viviendas == 0:
    raise ValueError("El total de viviendas es cero. Revisa el archivo de entrada.")

resumen["porcentaje_viviendas"] = 100 * resumen["viviendas"] / total_viviendas

(directorio / "resultados").mkdir(exist_ok=True)
(directorio / "figuras").mkdir(exist_ok=True)
resumen.to_csv(
    directorio / "resultados" / "resumen_ccaa.csv",
    index=False,
    encoding="utf-8-sig",
    float_format="%.2f",
)

# El gráfico incluye las comunidades y las ciudades autónomas del archivo.
grafico = resumen.iloc[::-1]
nombres = grafico["ccaa"].str.replace("_", " ", regex=False).replace(
    {
        "Andalucia": "Andalucía",
        "Aragon": "Aragón",
        "Castilla y Leon": "Castilla y León",
        "Cataluna": "Cataluña",
        "Pais Vasco": "País Vasco",
    }
)

figura, eje = plt.subplots(figsize=(11, 8))
barras = eje.barh(nombres, grafico["viviendas"], color="#26736C")
etiquetas = [f"{valor:,.0f}".replace(",", ".") for valor in grafico["viviendas"]]
eje.bar_label(barras, labels=etiquetas, padding=5, fontsize=9)
eje.set_xlim(0, grafico["viviendas"].max() * 1.2)
eje.set_title("Viviendas recogidas en el CSV por comunidad o ciudad autónoma")
eje.set_xlabel("Número de viviendas (suma de value)")
eje.set_axisbelow(True)
eje.grid(axis="x", alpha=0.2)
figura.text(
    0.02,
    0.02,
    "Fuente: Civio, CSV del proyecto. La cobertura temporal varía entre territorios.",
    fontsize=9,
)
figura.tight_layout(rect=(0, 0.05, 1, 1))
figura.savefig(directorio / "figuras" / "viviendas_por_ccaa.png", dpi=200)
plt.close(figura)

print(f"Filas del CSV: {datos.shape[0]}")
print(f"Columnas del CSV: {datos.shape[1]}")
print(f"Comunidades y ciudades autónomas: {len(resumen)}")
print(f"Años presentes: {datos['year'].min():.0f}-{datos['year'].max():.0f}")
print(f"Viviendas representadas: {total_viviendas:,.0f}")
print(resumen.round(2).to_string(index=False))
