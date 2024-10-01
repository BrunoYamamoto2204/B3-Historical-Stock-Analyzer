import json
import yfinance as yf

with open("tickers.json","r") as r:
    tickers_list = json.load(r)

start = input("Data start: ").strip().replace("/", "-")
start_br = start.split("-")
start_br = f"{start_br[2]}-{start_br[1]}-{start_br[0]}"

end = input("Data end: ").strip().replace("/", "-")
end_br = end.split("-")
end_br = f"{end_br[2]}-{end_br[1]}-{end_br[0]}"

for ticker in tickers_list:
    acao = yf.Ticker(ticker)
    historico_valor = acao.history(start=start_br,end=end_br)
    if historico_valor['Close'].iloc[0] >= 10:
        print(f"{ticker}: {historico_valor['Close'].iloc[0]:.2f}")

# 20/03/2024
# 20/09/2024