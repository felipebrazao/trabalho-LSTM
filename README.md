# Previsão diária de aluguéis com LSTM

Experimento de previsão do total de aluguéis do próximo dia com o Bike Sharing Dataset da UCI. Compara duas janelas de histórico, de 7 e 28 dias, e avalia a LSTM selecionada contra a persistência e a referência sazonal semanal.

O notebook inclui explicações, código, tabelas e gráficos da execução concluída. A declaração de uso de IA generativa está no início do notebook.

## Arquivos

| Caminho | Conteúdo |
| --- | --- |
| `LSTM.ipynb` | Notebook principal, com as saídas salvas |
| `day.csv` | Dados diários usados no experimento |
| `executar_notebook.py` | Executa o notebook inteiro e salva as saídas |
| `requirements.txt` | Versões das dependências usadas na execução local |
| `resultados_lstm/` | Métricas, previsões, gráfico, configuração, conclusão e modelo selecionado |

O ambiente virtual `.venv/` é local e não deve ser enviado ao GitHub. Os resultados do experimento são versionados para permitir a consulta sem executar o treinamento novamente.

## Executar no Google Colab

1. Abra `LSTM.ipynb` no Google Colab.
2. Envie `day.csv` para a área de arquivos ou permita que o notebook baixe a base da UCI.
3. Execute todas as células na ordem. Se faltar alguma biblioteca, use a instrução de instalação indicada na seção de ambiente do notebook.
4. Salve o notebook com as saídas após a execução.

## Executar localmente no Windows

A execução salva novamente o notebook e substitui os arquivos gerados em `resultados_lstm/`. A configuração utilizada foi Python 3.12.2. Hardware e versões podem afetar os resultados, mesmo com a semente fixa.

Na raiz do projeto, crie o ambiente, instale as dependências e registre o kernel:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m ipykernel install --user --name lstm-projeto --display-name "Python (LSTM - projeto)"
```

Para executar todas as células e salvar as saídas:

```powershell
.\.venv\Scripts\python.exe executar_notebook.py
```

Para executar pelo editor, abra `LSTM.ipynb` e selecione o kernel **Python (LSTM - projeto)**.

## Método

- Série diária de 2011 a 2012, com `cnt` como variável-alvo.
- Separação cronológica por data-alvo, reservando os últimos 20% para teste e os 20% anteriores para validação, com arredondamento para cima.
- Padronização ajustada somente no treino.
- Janelas deslizantes de 7 e 28 dias, com as mesmas datas-alvo e previsão de um passo à frente.
- Mesma arquitetura e hiperparâmetros para as duas redes.
- Escolha da janela pelo menor MAE de validação, na escala original.
- Avaliação final da LSTM selecionada, da persistência e da referência sazonal semanal nas mesmas datas de teste.

## Resultados salvos

MAE em aluguéis por dia; quanto menor, melhor.

| Janela | MAE de validação | Épocas executadas | Selecionada |
| --- | ---: | ---: | --- |
| 7 dias | 1.342,93 | 20 | Sim |
| 28 dias | 1.405,34 | 33 | Não |

| Método | MAE de teste |
| --- | ---: |
| Persistência | 878,39 |
| Sazonal semanal | 1.194,73 |
| LSTM de 7 dias | 1.481,34 |

A janela mais longa não melhorou o MAE de validação. No teste, a persistência teve o menor erro. O experimento utiliza uma única divisão temporal e uma semente, portanto não demonstra superioridade geral de um método.

As tabelas completas estão em `resultados_lstm/validacao.csv` e `resultados_lstm/teste.csv`. A pasta também contém as previsões por data, o gráfico de teste, o modelo `.keras`, a configuração e a conclusão numérica.

## Fonte dos dados

Fanaee-T, H. **Bike Sharing**. UCI Machine Learning Repository. DOI: https://doi.org/10.24432/C5W894.

Página da base: https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset. O arquivo `day.csv` é mantido no repositório para permitir a execução sem depender de um novo download.
