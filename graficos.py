import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set(style="whitegrid")


# Gráfico de Líneas
def crear_grafico_lineas():
    data = {
        "Día": [
            "Lunes",
            "Martes",
            "Miércoles",
            "Jueves",
            "Viernes",
            "Sábado",
            "Domingo",
        ],
        "Actividades": [5, 8, 6, 10, 7, 4, 2],
    }
    df = pd.DataFrame(data)

    plt.figure(figsize=(10, 5))
    sns.lineplot(data=df, x="Día", y="Actividades", marker="o", color="blue")
    plt.xlabel("Días")
    plt.ylabel("Cantidad de Actividades")
    plt.tight_layout()
    plt.savefig("img/graficos/linea.png")
    plt.close()


# Gráfico de Torta
def crear_grafico_torta():
    tipos = [
        "música",
        "deporte",
        "ciencias",
        "religión",
        "política",
        "tecnología",
        "juegos",
        "baile",
        "comida",
        "otro",
    ]
    cantidades = [12, 18, 8, 5, 9, 14, 11, 7, 6, 4]

    plt.figure(figsize=(8, 8))
    plt.pie(cantidades, labels=tipos, autopct="%1.1f%%", startangle=90)
    plt.axis("equal")
    plt.tight_layout()
    plt.savefig("img/graficos/torta.png")
    plt.close()


# Gráfico de Barras
def crear_grafico_barras():
    meses = [
        "Enero",
        "Febrero",
        "Marzo",
        "Abril",
        "Mayo",
        "Junio",
        "Julio",
        "Agosto",
        "Septiembre",
        "Octubre",
        "Noviembre",
        "Diciembre",
    ]

    data = {
        "Mes": meses * 3,
        "Turno": ["Mañana"] * 12 + ["Mediodía"] * 12 + ["Tarde"] * 12,
        "Actividades": [
            8,
            10,
            12,
            9,
            15,
            10,
            11,
            16,
            10,
            7,
            17,
            10,
            5,
            7,
            6,
            8,
            9,
            7,
            5,
            9,
            8,
            7,
            9,
            5,
            10,
            9,
            8,
            7,
            13,
            11,
            14,
            11,
            11,
            9,
            13,
            12,
        ],
    }
    df = pd.DataFrame(data)

    plt.figure(figsize=(20, 12))
    ax = sns.barplot(x="Mes", y="Actividades", hue="Turno", data=df, palette="Set2")
    plt.xlabel("Meses")
    plt.ylabel("Cantidad de Actividades")
    plt.tight_layout()
    plt.savefig("img/graficos/barras.png")
    plt.close()


if __name__ == "__main__":
    crear_grafico_lineas()
    crear_grafico_torta()
    crear_grafico_barras()
    print("Listo!")
