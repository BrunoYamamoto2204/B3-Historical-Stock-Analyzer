import yfinance as yf
import pandas as pd
import json
from datetime import datetime, timedelta

pd.set_option('display.max_rows', None)
def dias_nao_operacao_input(data_str):
    data = datetime.strptime(data_str, "%d-%m-%Y")
    # Subtrai 1 dia

    if data.weekday() == 6:
        data = data - timedelta(days=2)
    elif data.weekday() == 5:
        data = data - timedelta(days=1)

    # Retorna a data anterior no formato correto
    return data.strftime("%d-%m-%Y")
def dias_nao_operacao_ontem(data_str):
    # Converte a string de data para um objeto datetime
    data = datetime.strptime(data_str, "%Y-%m-%d")
    data = data - timedelta(days=1)
    # Subtrai 1 dia

    if data.weekday() == 6:
        data = data - timedelta(days=2)
    elif data.weekday() == 5:
        data = data - timedelta(days=1)

    # Retorna a data anterior no formato correto
    return data.strftime("%Y-%m-%d")

def resumo_acao(ticker,inicio_hoje,final_hoje,lucro_desejado,num_acao,por_gain,inicio_ontem,final_ontem,volume_medio_desj,gain_desej):

    data_inicio =  inicio_hoje.split("-")
    data_inicio = f"{data_inicio[2]}/{data_inicio[1]}/{data_inicio[0]}"

    data_final = final_hoje.split("-")
    data_final = f"{data_final[2]}/{data_final[1]}/{data_final[0]}"

    acao = yf.Ticker(ticker)
    qntd_lucro = 0 #Quantas ações ficaram acima da porcentagem desejada
    tot_fechamento = 0
    tot_abertura = 0
    lucro_max = -1000
    lucro_min = 1000

    qntd_gain = 0 #Trades que deram certo
    total_trades = 0 #Trades totais
    qntd_loss = 0 #Trades que deram errado
    max_gain = -100000
    min_gain = 1000000
    media_gain = 0

    qntd_dias = 0
    var_abertura = []
    var_maxima = []
    var_minima = []
    var_fechamento = []
    trade_caindo = [] #Resultado lucro/prejuizo ou não comprou
    trade_subindo = []

    try:
        historico_valores_hoje = acao.history(start= inicio_hoje,end=final_hoje)
        historico_valores_ontem = acao.history(start= inicio_ontem,end=final_ontem)
    except Exception as e:
        print(f"Erro ao obter dados de {ticker}: {e}")
        return None

    if historico_valores_hoje.empty or historico_valores_ontem.empty:
        print(f"Sem dados disponíveis para {ticker} no período especificado.")
        return None

    volume_medio = historico_valores_hoje["Volume"].mean()

    if volume_medio >= float(volume_medio_desj):
        historico_valores_hoje.rename(columns={"Open": "Abertura", "Close": "Fechamento", "Low": "Mais_baixo", "High": "Mais_alto"}, inplace=True)
        historico_valores_ontem.rename(columns={"Open": "Abertura", "Close": "Fechamento", "Low": "Mais_baixo", "High": "Mais_alto"}, inplace=True)


        for dia in range((len(historico_valores_ontem))):
            qntd_dias += 1
            fechamento_ontem = historico_valores_ontem['Fechamento'].iloc[dia] #Um dia a menos
            fechamento_hoje = historico_valores_hoje["Fechamento"].iloc[dia]
            abertura = historico_valores_hoje['Abertura'].iloc[dia]
            maxima = historico_valores_hoje["Mais_alto"].iloc[dia]
            minima = historico_valores_hoje["Mais_baixo"].iloc[dia]

            var_abertura.append((abertura/fechamento_ontem- 1) * 100)
            var_maxima.append((maxima/fechamento_ontem- 1) * 100)
            var_minima.append((minima/fechamento_ontem- 1) * 100)
            var_fechamento.append((fechamento_hoje/fechamento_ontem-1) * 100)

            if por_gain < 0: #
                if var_abertura[dia] < por_gain: #Se abertura for menor que a ordem, compra na abertura
                    trade_caindo.append(var_fechamento[dia] - var_abertura[dia])
                    total_trades += 1
                    if trade_caindo[dia] >= 0:
                        qntd_gain += 1
                    else:
                        qntd_loss += 1
                elif var_minima[dia] < por_gain: #Caso nao compre na abertura, verificar se a minima chegou, caso sim compra na ordem
                    trade_caindo.append(var_fechamento[dia] - por_gain)
                    total_trades += 1
                    if trade_caindo[dia] >= 0:
                        qntd_gain += 1
                    else:
                        qntd_loss += 1
                else:
                    trade_caindo.append(None)

            elif por_gain > 0: #Isso aqui é para venda subindo, mas se inverter algumas coisas atende a compra subindo
                if var_abertura[dia] > por_gain:
                    trade_subindo.append(var_abertura[dia] - var_fechamento[dia])
                    total_trades += 1
                    if trade_subindo[dia] >= 0:
                        qntd_gain += 1
                    else:
                        qntd_loss += 1
                elif var_maxima[dia] > por_gain:
                    trade_subindo.append(por_gain - var_fechamento[dia])
                    total_trades += 1
                    if trade_subindo[dia] >= 0:
                        qntd_gain += 1
                    else:
                        qntd_loss += 1
                else:
                    trade_subindo.append(None)

            #MAX E MIN GAIN
            if por_gain < 0:
                if isinstance(trade_caindo[dia], (int,float)):
                    if trade_caindo[dia] > max_gain:
                        max_gain = trade_caindo[dia]
                    if trade_caindo[dia] < min_gain:
                        min_gain = trade_caindo[dia]
            else:
                if isinstance(trade_subindo[dia], (int,float)):
                    if trade_subindo[dia] > max_gain:
                        max_gain = trade_subindo[dia]
                    if trade_subindo[dia] < min_gain:
                        min_gain = trade_subindo[dia]

            # # CONFERE OS VALORES DE VARIACAO
            # print(f"Var abertura: {var_abertura[dia]:.2f}")
            # print(f"Var minima: {var_minima[dia]:.2f}")
            # print(f"Var fechamento: {var_fechamento[dia]:.2f}")
            # if isinstance(trade_caindo[dia], (int,float)):
            #     print(f"Trade caindo: {trade_caindo[dia]:.2f}")
            # else:
            #     print(f"Trade caindo: {trade_caindo[dia]}")
            # print("-"*40)
            #
            # #VALORES COM AS DATAS RESPECTIVAS
            # print(f"Fechamento ontem: {historico_valores_ontem.index[dia].strftime('%Y-%m-%d')} - {fechamento_ontem}")
            # print(f"Fechamento hoje: {historico_valores_hoje.index[dia].strftime('%Y-%m-%d')} - {fechamento_hoje}")
            # print(f"Variacao = {var_fechamento[dia]:.2f}%")

            tot_abertura += abertura
            tot_fechamento += fechamento_hoje

            #MAX E MIN LUCRO (NO PERÍODO)
            lucro = ((fechamento_hoje - abertura)/abertura)*100
            if lucro >= float(lucro_desejado):
                qntd_lucro += 1 #quantidade de quantos atendeu ao lucro
            if lucro > lucro_max:
                lucro_max = lucro
            if lucro < lucro_min:
                lucro_min = lucro

        #MEDIA GAIN
        soma_gain = 0
        cont_num_media = 0
        if por_gain < 0:
            for c in trade_caindo:
                if isinstance(c, (int, float)):
                    soma_gain += c #Só essa soma serve para o resultado gain
                    cont_num_media += 1
        else:
            for c in trade_subindo:
                if isinstance(c, (int, float)):
                    soma_gain += c #Só essa soma serve para o resultado gain
                    cont_num_media += 1
        try:
            media_gain = soma_gain/cont_num_media
        except ZeroDivisionError:
            media_gain = 0


        if qntd_dias == 0:
            print(f"Sem dados suficientes para {ticker}.")
            return None

        #PORCENTAGEM DE GAIN
        if total_trades > 0:
            gain = (qntd_gain / total_trades) * 100
        else:
            gain = 0

        # PORCENTAGEM DE LOSS
        if total_trades > 0:
            loss = (qntd_loss / total_trades) * 100
        else:
            loss = 0

        por_atendida = (qntd_lucro/qntd_dias) * 100 #porcentagem de quantos atendeu ao lucro
        tot_lucro = ((tot_fechamento - tot_abertura)/tot_abertura)*100


        if gain >= gain_desej:
            print("="*60)
            print(f"{num_acao+1} - ({data_inicio} - {data_final}) - \033[34m{ticker}\033[m - R${volume_medio:.2f}")

            if tot_lucro > 0:
                print(f"\033[32mLucro: {tot_lucro:.2f}%\033[m")
            else:
                print(f"\033[31mLucro: {tot_lucro:.2f}%\033[m")


            if por_gain < 0:
                print("-" * 30)
                print(f"Lucro \033[32mMÁXIMO:\033[m \033[32m{lucro_max:.2f}%\033[m")
                print(f"Lucro \033[31mMÍNIMO:\033[m \033[31m{lucro_min:.2f}%\033[m")
                print(f"\033[1;4;34mTotal Trades:\033[m \033[36m{total_trades}\033[m")

                print(f"\033[34mGain trades:\033[m \033[36m{qntd_gain}\033[m")
                print(f"\033[34mLoss trades:\033[m \033[36m{qntd_loss}\033[m")
                print(f"Porcentagem de \033[4;32mGain(%):\033[m \033[33m{gain:.2f}%\033[m")
                print(f"Porcentagem de \033[4;31mLoss(%):\033[m \033[33m{loss:.2f}%\033[m")

                print(f"\033[32mMax\033[m Gain: \033[34m{max_gain:.2f}%\033[m")
                print(f"\033[31mMin\033[m Gain: \033[34m{min_gain:.2f}%\033[m")
                print(f"\033[33mMédia Gain:\033[m \033[34m{media_gain:.2f}%\033[m")

                print("-" * 30)
                print(f"RESULTADO GAIN: \033[36m{soma_gain:.2f}%\033[m")
                print(f"Porcentagem de ações igual ou acima de {lucro_desejado}% = \033[36m{por_atendida:.2f}%\033[m")
                print("=" * 60)
                print()

            else:
                print("-" * 30)
                print(f"Lucro \033[32mMÁXIMO:\033[m \033[32m{lucro_max:.2f}%\033[m")
                print(f"Lucro \033[31mMÍNIMO:\033[m \033[31m{lucro_min:.2f}%\033[m")
                print(f"\033[1;4;34mTotal Trades:\033[m \033[36m{total_trades}\033[m")

                print(f"\033[34mGain trades:\033[m \033[36m{qntd_loss}\033[m")
                print(f"\033[34mLoss trades:\033[m \033[36m{qntd_gain}\033[m")
                print(f"Porcentagem de \033[4;32mGain(%):\033[m \033[33m{loss:.2f}%\033[m")
                print(f"Porcentagem de \033[4;31mLoss(%):\033[m \033[33m{gain:.2f}%\033[m")

                print(f"\033[32mMax\033[m Gain: \033[34m{(min_gain*-1):.2f}%\033[m")
                print(f"\033[31mMin\033[m Gain: \033[34m{(max_gain*-1):.2f}%\033[m")
                print(f"\033[33mMédia Gain:\033[m \033[34m{(media_gain*-1):.2f}%\033[m")

                print("-" * 30)
                print(f"RESULTADO GAIN: \033[36m{(soma_gain*-1):.2f}%\033[m")
                print(f"Porcentagem de ações igual ou acima de {lucro_desejado}% = \033[36m{por_atendida:.2f}%\033[m")
                print("=" * 60)
                print()

        return gain

