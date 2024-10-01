import yfinance as yf
import pandas as pd
import json
pd.set_option('display.max_rows', None)

with open("tickers.json","r") as r:
    tickers_list = json.load(r)

ticker = "ITSA4.SA"
acao = yf.Ticker(ticker)

start = input("Data start: ").strip().replace("/","-")
start_br = start.split("-")
start_br = f"{start_br[2]}-{start_br[1]}-{start_br[0]}"

end = input("Data end: ").strip().replace("/","-")
end_br = end.split("-")
end_br = f"{end_br[2]}-{end_br[1]}-{end_br[0]}"

historico_valores = acao.history(start= start_br,end=end_br)
historico_valores.rename(columns={"Open": "Abertura", "Close": "Fechamento", "Low": "Mais baixo", "High": "Mais alto"}, inplace=True)
print(historico_valores[['Abertura', 'Fechamento', 'Mais alto', 'Mais baixo']])

valor_start = historico_valores["Fechamento"].iloc[0]
valor_end = historico_valores["Fechamento"].iloc[-1]
print(f"Preço inicial: {valor_end:.2f}")
print(f"Preço final: {valor_start:.2f}")
print(ticker)
volume_medio = historico_valores['Volume'].mean()
print(f"Volume médio: R${volume_medio:.2f}")
print(f"Diferença de valorização: {valor_start-valor_end}")
