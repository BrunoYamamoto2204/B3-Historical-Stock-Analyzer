import json
import yfinance as yf
import Todos_valores_acao
import time

with open("tickers.json","r") as r:
    tickers_list = json.load(r)

print("\033[33m*Caso todas as ações estajam dando gain 100%, reinicie o código e insira outra data próxima.\033[m")
print("\033[33m*As ações demoram cerca de 3:30s  a 4:30s para carregar.\033[m")
print("\033[33m*Procure usar mais ordens de compra negativos\n\033[m")

start = Todos_valores_acao.dias_nao_operacao_input(input("Data start: ").strip().replace("/", "-"))
start_br = start.split("-")
start_br_hoje = f"{start_br[2]}-{start_br[1]}-{start_br[0]}"
start_br_ontem = Todos_valores_acao.dias_nao_operacao_ontem(f"{start_br[2]}-{start_br[1]}-{(start_br[0])}")

end = Todos_valores_acao.dias_nao_operacao_input(input("Data end: ").strip().replace("/", "-"))
end_br = end.split("-")
end_br_hoje = f"{end_br[2]}-{end_br[1]}-{end_br[0]}"
end_br_ontem = Todos_valores_acao.dias_nao_operacao_ontem(f"{end_br[2]}-{end_br[1]}-{(end_br[0])}")

lucro_acoes=[]
por_lucro = input("Margem de lucro desejada(%): ")
por_gain = input("Ordem de compra, para calcular gain(%): ")
por_gain = float(por_gain)
volume_medio_desj = input("Volume médio: R$")
gain_desej = float(input("Gain desejado, acima de(%): "))

lista_crescente_volume_ticker = []
lista_crescente_volume_valor = []

start_time = time.time()
for e,ticker in enumerate(tickers_list):
    gain = Todos_valores_acao.resumo_acao(ticker,start_br_hoje,end_br_hoje,por_lucro,e,por_gain,start_br_ontem,end_br_ontem,volume_medio_desj,gain_desej) #Lucro total de cada acao

    if gain is None:
        continue

    posicao = 0
    while posicao < len(lista_crescente_volume_valor) and gain > lista_crescente_volume_valor[posicao]:
        posicao += 1
    lista_crescente_volume_valor.insert(posicao,gain)
    lista_crescente_volume_ticker.insert(posicao, ticker)

end_time = time.time()

seg = end_time - start_time
min = 0

if seg >= 60:
    min = int(seg // 60)
    seg = int(seg % 60)

print(f"Tempo para carregar ações: {min}:{seg}")

ver_acao = 1
while int(ver_acao) != 0:
    print("\033[1;4;34mAÇÕES FILTRADAS:\033[m")
    for e,c in enumerate(lista_crescente_volume_valor):
        if c >= gain_desej:
            print(f"\033[34m{lista_crescente_volume_ticker[e]}\033[m - \033[33m{c:.2f}%\033[m")
    while True:
        ver_acao = input("""\n- Ver qual ação?(.SA) 
- Terminar - (0)
- Ver ações - (1)
                              
Escolha: """).strip().upper()
        if ver_acao == "0" or ver_acao == "1":
            break
        elif ver_acao not in lista_crescente_volume_ticker:
            print("\033[31mAção não encontrada! Tente novamente\033[m")
        else:
            Todos_valores_acao.resumo_acao(ver_acao, start_br_hoje, end_br_hoje, por_lucro, e, por_gain, start_br_ontem,end_br_ontem, volume_medio_desj, gain_desej)






# 20/06/2024
# 20/09/2024

#22/04/2024
#24/09/2024



