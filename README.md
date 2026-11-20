# Previsão diária de aluguéis com LSTM

Experimento com o Bike Sharing Dataset da UCI para prever o total de aluguéis do próximo dia. Todo o código, as explicações, as tabelas, os gráficos e as conclusões estão em **LSTM.ipynb**, com as saídas da execução salvas. O notebook não exporta CSVs, imagens, configurações ou modelos separados.

## Arquivos

| Arquivo | Conteúdo |
| --- | --- |
| `LSTM.ipynb` | Notebook completo, incluindo resultados e comparação final |
| `day.csv` | Dados diários utilizados no experimento |
| `requirements.txt` | Versões das dependências da execução local |
| `executar_notebook.py` | Execução pelo terminal, salvando as saídas no próprio notebook |
| `README.md` | Instruções e descrição do projeto |

O ambiente `.venv/` é local e não deve ser enviado ao GitHub ou incluído na entrega. Os arquivos de configuração do Git também são mantidos.

## Executar no Google Colab

1. Abra `LSTM.ipynb` no Google Colab.
2. Envie `day.csv` ou permita que o notebook baixe a base da UCI, caso o arquivo não exista.
3. Execute todas as células na ordem. Se necessário, use `%pip install tensorflow numpy pandas matplotlib`.
4. Salve o notebook com as saídas após a execução.

## Executar localmente no Windows

O ambiente utilizado foi Python 3.12.2. Hardware e versões podem afetar os resultados, mesmo com semente fixa. Para preparar o ambiente:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m ipykernel install --user --name lstm-projeto --display-name "Python (LSTM - projeto)"
```

Para executar tudo e salvar as saídas em `LSTM.ipynb`:

```powershell
.\.venv\Scripts\python.exe executar_notebook.py
```

No editor, abra o notebook e selecione o kernel **Python (LSTM - projeto)**. Para consultar as saídas já salvas, não é necessário treinar novamente. Para utilizar as redes em uma nova sessão, execute o treinamento; os modelos são mantidos apenas em memória durante a execução.

## Método e organização do notebook

- **Seções 1 a 6:** preparação dos dados, separação cronológica, normalização somente no treino e LSTM original com janelas de 7 e 28 dias. Avaliação contra persistência e referência sazonal semanal.
- **Seção 7:** heatmap exploratório do treino e análise empírica das features escolhidas: `cnt`, dia da semana e feriado. Uma LSTM com janela de 7 dias e 8 features por passo é treinada.
- **Seção 8:** apresentação dos hiperparâmetros escolhidos, treinamento da LSTM direta ajustada e da residual, curvas das quatro redes e comparação final dos seis métodos.

As últimas duas parcelas de 20% da série são reservadas para validação e teste, com arredondamento para cima. Todas as configurações usam as mesmas datas-alvo; os primeiros 28 dias fornecem contexto. O cenário representa previsões diárias sucessivas de um passo, atualizando o histórico com as observações já disponíveis.

As escolhas de features e hiperparâmetros são empíricas. O notebook apresenta somente as configurações utilizadas, sem grades de busca, rankings de candidatos ou repetições em várias sementes. A validação cronológica permanece necessária para a parada antecipada e a restauração dos melhores pesos. Todas as redes usam a semente 42.

## Configurações apresentadas

| Rede | Entrada | Janela | Unidades LSTM | Máximo de épocas | Paciência |
| --- | --- | ---: | ---: | ---: | ---: |
| Original | `cnt` | 7 dias | 32 | 100 | 12 |
| Com features | `cnt` + dia da semana + feriado | 7 dias | 32 | 100 | 12 |
| Hiperparâmetros alterados | `cnt` | 7 dias | 64 | 150 | 25 |
| Residual | `cnt` | 28 dias | 32 | 150 | 25 |

Todas usam Dense 16 ReLU, saída linear, Adam com taxa inicial 0,001, lote 32 e perda MAE. As versões ajustada e residual reduzem a taxa pela metade após 7 épocas sem melhora, até o mínimo de 0,00001. A residual prevê **aluguel de ontem + correção aprendida**, uma mudança de arquitetura que deve ser distinguida do ajuste de hiperparâmetros.

A versão com features considera os padrões semanais e as mudanças de rotina nos feriados. São seis indicadores de dia da semana, um de feriado e o histórico de `cnt`, totalizando 8 features por passo. O calendário do dia previsto já é conhecido. Nenhum valor de `cnt` do dia previsto é usado como entrada. O clima observado desse dia, `casual`, `registered` e `instant` são excluídos.

## Resultados da execução salva

| Rede | MAE de validação, semente 42 |
| --- | ---: |
| LSTM original | 1.342,93 |
| LSTM com features | 1.227,32 |
| LSTM com hiperparâmetros alterados | 1.148,08 |
| LSTM residual | 894,63 |

| Método | MAE de teste |
| --- | ---: |
| LSTM residual | 874,13 |
| Persistência | 878,39 |
| Sazonal semanal | 1.194,73 |
| LSTM com hiperparâmetros alterados | 1.296,45 |
| LSTM com features | 1.354,61 |
| LSTM original | 1.481,34 |

O MAE está em aluguéis por dia; quanto menor, melhor. A residual apresentou o menor erro nesta avaliação, mas sua vantagem sobre a persistência foi de aproximadamente 0,49%. As conclusões se limitam a uma semente e a esta divisão temporal. Como o teste já foi consultado durante a exploração, a comparação é descritiva e não demonstra superioridade geral. As tabelas, os parâmetros e os gráficos estão no próprio notebook.

## Referências

- Fanaee-T, H. **Bike Sharing**. UCI Machine Learning Repository. [Dataset e descrição](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset). DOI: https://doi.org/10.24432/C5W894.
- [TensorFlow: séries temporais](https://www.tensorflow.org/tutorials/structured_data/time_series).
- [TensorFlow: overfit e underfit](https://www.tensorflow.org/tutorials/keras/overfit_and_underfit).
- [Keras: ReduceLROnPlateau](https://keras.io/api/callbacks/reduce_lr_on_plateau/).
