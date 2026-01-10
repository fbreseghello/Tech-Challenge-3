## Sobre o Projeto

Este projeto é parte do **Tech Challenge**, que aplica técnicas avançadas de Machine Learning (supervisionado e não supervisionado) para analisar e prever atrasos de voos nos Estados Unidos. O objetivo é desenvolver um pipeline completo de ciência de dados, desde a exploração até a interpretação dos resultados.

### Objetivos

1. **Análise Exploratória de Dados (EDA)**: Investigar os dados com estatísticas descritivas e visualizações
2. **Modelagem Supervisionada**: 
   - Classificação: Prever se um voo vai atrasar ou não
   - Regressão: Prever quanto tempo o atraso vai durar
3. **Modelagem Não Supervisionada**: 
   - Clusterização: Agrupar aeroportos, rotas e companhias aéreas
   - Redução de Dimensionalidade: PCA para visualização e análise

## Datasets

O projeto utiliza três arquivos CSV:

1. **airlines.csv**: 14 companhias aéreas (IATA_CODE, AIRLINE) ✅ Incluído no repositório
2. **airports.csv**: 322 aeroportos (IATA_CODE, AIRPORT, CITY, STATE, COUNTRY, LATITUDE, LONGITUDE) ✅ Incluído no repositório
3. **flights.csv**: ~5,8 milhões de registros de voos (565 MB) ⚠️ **Não incluído** - muito grande para GitHub


## Notebooks e Análises

### 1. Análise Exploratória de Dados (EDA)

**Arquivo**: `01_EDA_Analise_Exploratoria.ipynb`

**Conteúdo**:
- Carregamento e visão geral dos dados
- Estatísticas descritivas
- Análise de valores ausentes e tratamento
- Análise temporal (por mês, dia da semana, horário)
- Análise por companhia aérea
- Análise por aeroporto (identificação de aeroportos críticos)
- Análise de distância e tempo de voo
- Matriz de correlação
- Principais insights e conclusões

**Principais Visualizações**:
- Distribuições de voos por período
- Aeroportos mais críticos (maior atraso)
- Comparação entre companhias aéreas
- Padrões de atraso ao longo do tempo

### 2. Modelagem Supervisionada

**Arquivo**: `02_Modelagem_Supervisionada.ipynb`

#### Classificação (Prever se voo vai atrasar)

**Modelos Testados**:
- Logistic Regression
- Random Forest
- Gradient Boosting
- XGBoost
- LightGBM

**Métricas de Avaliação**:
- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC

#### Regressão (Prever tempo de atraso)

**Modelos Testados**:
- Linear Regression
- Ridge Regression
- Random Forest Regressor
- Gradient Boosting Regressor
- XGBoost Regressor
- LightGBM Regressor

**Métricas de Avaliação**:
- MAE (Mean Absolute Error)
- MSE (Mean Squared Error)
- RMSE (Root Mean Squared Error)
- R² Score

**Features Engineering**:
- Período do dia (Madrugada, Manhã, Tarde, Noite)
- Indicador de final de semana
- Trimestre/Estação do ano
- Categoria de distância
- Tempo de voo programado

### 3. Modelagem Não Supervisionada

**Arquivo**: `03_Modelagem_Nao_Supervisionada.ipynb`

#### Clusterização

**Análises Realizadas**:
1. **Clusterização de Aeroportos**: Agrupamento baseado em volume de voos, taxa de atraso, distância média
2. **Clusterização de Companhias Aéreas**: Perfis operacionais similares
3. **Clusterização de Rotas**: Identificação de rotas problemáticas vs eficientes

**Técnicas**:
- K-Means
- Método do Cotovelo (Elbow Method)
- Silhouette Score

**Métricas de Qualidade**:
- Silhouette Score
- Calinski-Harabasz Score
- Davies-Bouldin Score

#### Redução de Dimensionalidade

**Técnicas**:
- PCA (Principal Component Analysis)
- Análise de variância explicada
- Visualização 2D dos clusters

## Principais Resultados

### Insights da EDA

1. **Padrões Temporais**: Atrasos são mais comuns em determinados meses e dias da semana
2. **Aeroportos Críticos**: Identificação de hubs com maiores problemas de pontualidade
3. **Companhias Aéreas**: Variação significativa no desempenho entre operadoras
4. **Correlações**: Relação entre distância, horário e probabilidade de atraso

### Modelos Supervisionados

- **Melhor Modelo de Classificação**: [Será preenchido após execução]
- **Melhor Modelo de Regressão**: [Será preenchido após execução]
- **Features Mais Importantes**: Horário de partida, aeroporto de origem, companhia aérea

### Clusterização

- **Aeroportos**: Identificados X clusters com perfis distintos (hubs principais, regionais, problemáticos)
- **Companhias**: Agrupadas por padrões operacionais similares
- **Rotas**: Categorização baseada em eficiência e volume

## Perguntas Respondidas

✅ **Quais aeroportos são mais críticos em relação a atrasos?**
- Análise detalhada no notebook de EDA com ranking de aeroportos

✅ **Que características aumentam a chance de atraso em um voo?**
- Feature importance nos modelos de classificação

✅ **Os atrasos são mais comuns em certos dias da semana ou horários?**
- Análise temporal completa no EDA

✅ **É possível agrupar aeroportos com perfis semelhantes?**
- Clusterização de aeroportos com visualização PCA

✅ **Até que ponto conseguimos prever atrasos?**
- Métricas de performance dos modelos supervisionados

## Tecnologias Utilizadas

### Análise de Dados
- **Pandas**: Manipulação de dados
- **NumPy**: Operações numéricas

### Visualização
- **Matplotlib**: Gráficos estáticos
- **Seaborn**: Visualizações estatísticas
- **Plotly**: Gráficos interativos

### Machine Learning
- **Scikit-learn**: Modelos e métricas
- **XGBoost**: Gradient Boosting otimizado
- **LightGBM**: Gradient Boosting eficiente
- **Imbalanced-learn**: Tratamento de desbalanceamento

### Ambiente
- **Jupyter Notebook**: Desenvolvimento interativo



- **Felipe Breseghello**

