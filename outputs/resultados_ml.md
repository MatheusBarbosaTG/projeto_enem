# Resultados de Machine Learning (nível município)

Alvo: nota média do município. 1,801 municípios; validação cruzada 5-fold.

## Regressão
| Modelo | MAE (pontos) | R² |
|---|---|---|
| Baseline (média) | 24.0 | -0.001 |
| Regressão Ridge | 7.2 | 0.899 |
| Gradient Boosting | 7.6 | 0.889 |

## Importância das variáveis
|                     |   importancia |
|:--------------------|--------------:|
| PCT_COMPUTADOR      |        0.8529 |
| UF                  |        0.0986 |
| PCT_ESCOLA_PRIVADA  |        0.0724 |
| PCT_PRETA_PARDA     |        0.0484 |
| PCT_WIFI            |        0.0282 |
| PCT_RENDA_ATE_1SM   |        0.0237 |
| PCT_RENDA_ACIMA_5SM |        0.0119 |
| PCT_MAE_SUPERIOR    |        0.0083 |
| PCT_PAI_SUPERIOR    |        0.0059 |
| PCT_FEMININO        |        0.0008 |
| RENDA_MEDIA_ORD     |       -0.002  |

## Clusterização (KMeans) de municípios
Silhouette por k: {2: 0.454, 3: 0.329, 4: 0.242, 5: 0.211, 6: 0.218}; k escolhido = 2.
|   CLUSTER |   RENDA_MEDIA_ORD |   PCT_RENDA_ATE_1SM |   PCT_RENDA_ACIMA_5SM |   PCT_MAE_SUPERIOR |   PCT_PAI_SUPERIOR |   PCT_FEMININO |   PCT_PRETA_PARDA |   PCT_ESCOLA_PRIVADA |   PCT_WIFI |   PCT_COMPUTADOR |   NOTA_MEDIA |   municípios |
|----------:|------------------:|--------------------:|----------------------:|-------------------:|-------------------:|---------------:|------------------:|---------------------:|-----------:|-----------------:|-------------:|-------------:|
|         0 |               3.5 |                28.8 |                  10.1 |               21.9 |               12.8 |           59.1 |              43.2 |                 18.6 |       93.8 |             55.2 |        547.5 |          813 |
|         1 |               1.5 |                71.3 |                   1.8 |               12   |                5   |           59.6 |              73.2 |                  5.4 |       78.3 |             24.5 |        505.1 |          988 |

## Observações
O modelo descreve associações entre municípios (nível ecológico), não causalidade, e não deve ser usado para julgar indivíduos ou escolas. Machine Learning no nível individual foi considerado inadequado porque PARTICIPANTES e RESULTADOS não podem ser ligados por participante.