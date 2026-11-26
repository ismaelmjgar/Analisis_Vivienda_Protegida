from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# 1. Lectura del dataset
df = pd.read_csv(
    "viviendas.csv",
    sep=None,
    engine="python",
    encoding="utf-8-sig"
)

# 2. Carpetas de resultados
Path("figuras").mkdir(exist_ok=True)
Path("resultados").mkdir(exist_ok=True)

# 3. Exploración inicial
print("Filas:", df.shape[0])
print("Columnas:", df.shape[1])

print("\nTipos de datos:")
print(df.dtypes)

print("\nValores ausentes:")
print(df.isna().sum())

# 4. Estadística descriptiva
numericas = df.select_dtypes(include="number")

if not numericas.empty:
    estadisticas = numericas.describe().T

    print("\nEstadística descriptiva:")
    print(estadisticas)

    estadisticas.to_csv(
        "resultados/estadistica.csv"
    )

# 5. Frecuencias de las variables
frecuencias = []

for columna in df.columns:
    texto = df[columna].value_counts().head(5)

    frecuencias.append(
        f"\n{columna}\n{texto.to_string()}"
    )

Path("resultados/frecuencias.txt").write_text(
    "\n".join(frecuencias),
    encoding="utf-8"
)

# 6. Histograma de una variable numérica
if not numericas.empty:
    columna = numericas.columns[0]

    numericas[columna].dropna().hist(bins=20)

    plt.title(f"Distribución de {columna}")
    plt.xlabel(columna)
    plt.ylabel("Frecuencia")
    plt.tight_layout()
    plt.savefig("figuras/histograma.png", dpi=200)
    plt.close()

# 7. Frecuencias de una variable categórica
categoricas = df.select_dtypes(exclude="number")

if not categoricas.empty:
    columna = categoricas.columns[0]

    df[columna].value_counts().head(10).plot.bar()

    plt.title(f"Frecuencias de {columna}")
    plt.ylabel("Número de registros")
    plt.tight_layout()
    plt.savefig("figuras/frecuencias.png", dpi=200)
    plt.close()

print("\nAnálisis finalizado.")