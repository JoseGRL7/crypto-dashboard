import requests
from flask import Flask, render_template, request
import yfinance as yf
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    url = "https://api.coinpaprika.com/v1/tickers"
    tickers = requests.get(url).json()

    cryp = None
    coins = []

    # Ordenamos por ranking
    sorted_coins = sorted(tickers, key=lambda x: x["rank"])

    # Guardamos solo símbolo para el selector
    for coin in sorted_coins[:30]:
        coins.append({"symbol": coin["symbol"]})

    # Si se selecciona moneda en formulario
    if request.method == "POST":
        coin_id = request.form.get("moneda")
        crypto = yf.Ticker(coin_id + "-USD")
        cryp = crypto.info

        # 🔹 Obtener histórico (últimos 30 días)
        hist = crypto.history(period="1mo")

        if not hist.empty:
            # Generar gráfica con tema oscuro
            fig, ax = plt.subplots(figsize=(6,4))
            fig.patch.set_facecolor("#121212")   # Fondo de la figura
            ax.set_facecolor("#121212")          # Fondo del gráfico

            ax.plot(hist.index, hist["Close"], color="white", label="Precio de Cierre", linewidth=2)

            # Colores de los ejes y etiquetas
            ax.tick_params(colors="white")
            ax.xaxis.label.set_color("white")
            ax.yaxis.label.set_color("white")
            ax.title.set_color("white")

            # Títulos
            ax.set_title(f"Histórico de {coin_id}/USD (30 días)")
            ax.set_xlabel("Fecha")
            ax.set_ylabel("Precio (USD)")

            # Leyenda con estilo oscuro
            legend = ax.legend()
            for text in legend.get_texts():
                text.set_color("white")
            legend.get_frame().set_facecolor("#1e1e1e")

            # Crear carpeta static si no existe
            if not os.path.exists("static"):
                os.makedirs("static")

            # Guardar gráfica
            plt.savefig("static/grafico.png", bbox_inches="tight", facecolor=fig.get_facecolor())
            plt.close()
        else:
            print("⚠️ No se encontraron datos históricos para", coin_id)

    return render_template("index.html", coins=coins, titulo="Top 30 Criptomonedas", cryp=cryp)

if __name__ == "__main__":
    app.run(debug=True)
