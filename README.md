# B3-Historical-Stock-Analyzer
Ferramenta em Python coleta dados históricos das ações da B3 baseado em períodos personalizados pelo usuário, utilizando a API yfinance. Fornece uma análise detalhada das ações  
  

### -- Funcionalidades --
- Busca cotações históricas com base em períodos pesonalizados 
- Integração com a API _yfinance_ para obter dados atualizados
- Mostra várias estatísticas sobre o desempenho das ações no período
- Permite a visualização das ações desejadas, separadamente 
- Permite inserir outros parâmetros como porcentagem de ordem de compra, margem de lucro e porcentagem de ganho desejado

### -- Input -- 
O programa solicitará os seguintes inputs:

- Período de análise (data inicial e data final)
- Porcentagem de ordem de compra
- Lucro desejado
- Volume médio
- Gain desejado

### -- Output --
- Lucro máximo e mínimo 
- Ganho máximo, mínimo e médio
- Quantidade de trades
- Resultado do Ganho e porcentagem de ações que atendem ao lucro desejado 

### --Observações-- 
- Bibliotecas = [ yfinance, json, pandas, datetime ] 
- Arquivos Funcionais = [ Todos_valores_acao.py e main.py ]
- Arquivos Testes [ Investimento_1.py e For_acoes.py ] 