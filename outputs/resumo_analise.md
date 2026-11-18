# Resumo da análise dos microdados do ENEM 2025 (gerado automaticamente)

Nível participante: 3,073,011 participantes com notas válidas. Nível município: 1,801 municípios com dados socioeconômicos (arquivo PARTICIPANTES) e de desempenho (arquivo RESULTADOS). Os dois arquivos não têm chave individual comum; por isso a relação entre perfil socioeconômico e nota é analisada por município (análise ecológica).

## Estatísticas descritivas das notas (0 a 1000)
|                      |       count |   mean |   median |   min |     max |    std |
|:---------------------|------------:|-------:|---------:|------:|--------:|-------:|
| Ciências da Natureza | 3.07301e+06 | 503.19 |   501.4  |     0 |  858.7  |  77.99 |
| Ciências Humanas     | 3.07301e+06 | 517.79 |   520.5  |     0 |  856.4  |  85.99 |
| Linguagens e Códigos | 3.07301e+06 | 538    |   543.5  |     0 |  794.5  |  69.39 |
| Matemática           | 3.07301e+06 | 525.02 |   506.7  |     0 |  980.3  | 127.67 |
| Redação              | 3.07301e+06 | 622.98 |   620    |    40 | 1000    | 157.43 |
| Nota média           | 3.07301e+06 | 541.4  |   533.56 |    56 |  862.96 |  85.67 |

## Nota média por rede (pública x privada)
| REDE    |   count |   mean |   median |   std |
|:--------|--------:|-------:|---------:|------:|
| Privada |  249577 | 612.72 |   616.68 | 80.75 |
| Pública |  955375 | 516.25 |   510.56 | 74.94 |

## Nota média por dependência administrativa
| DEPENDENCIA   |   count |   mean |   median |   std |
|:--------------|--------:|-------:|---------:|------:|
| Federal       |   66883 | 587.89 |   589.92 | 76.77 |
| Estadual      |  882055 | 510.61 |   505.46 | 71.9  |
| Municipal     |    6437 | 544.46 |   542.96 | 73.18 |
| Privada       |  249577 | 612.72 |   616.68 | 80.75 |

## Nota média por localização da escola
| LOCALIZACAO   |           count |   mean |   median |   std |
|:--------------|----------------:|-------:|---------:|------:|
| Rural         | 56024           | 500.36 |   491.28 | 76.09 |
| Urbana        |     1.14893e+06 | 537.98 |   530.68 | 85.68 |

## Nota média por UF da prova
| UF   |   count |   mean |   median |   std |
|:-----|--------:|-------:|---------:|------:|
| AM   |   53622 | 504.66 |   493.32 | 77.86 |
| PA   |  174185 | 506.26 |   494.56 | 79.11 |
| MA   |  131679 | 509.28 |   498.64 | 79.81 |
| AP   |   19772 | 512.73 |   503.22 | 76.3  |
| AC   |   16789 | 515.24 |   505.38 | 78.43 |
| RO   |   27172 | 519.62 |   512.73 | 75.29 |
| TO   |   22917 | 520.56 |   510.42 | 81.45 |
| BA   |  267541 | 521.74 |   512    | 81.2  |
| PI   |   80024 | 522.05 |   508.92 | 88.14 |
| RR   |    7468 | 525.19 |   515.43 | 81.1  |
| AL   |   60217 | 525.64 |   515.6  | 83.99 |
| SE   |   52851 | 532.33 |   522.18 | 86.4  |
| MT   |   44480 | 533.35 |   525.17 | 83.31 |
| MS   |   36051 | 534.23 |   524.2  | 83.63 |
| PE   |  177596 | 534.26 |   526    | 82.45 |
| CE   |  188182 | 537.58 |   531.08 | 87.15 |
| PB   |   93396 | 537.66 |   528.72 | 84.08 |
| RN   |   77831 | 541.71 |   533.24 | 84.13 |
| GO   |  106299 | 545.25 |   537.8  | 85.46 |
| PR   |  128057 | 550.14 |   543.64 | 81.6  |
| RJ   |  214021 | 553.6  |   546.54 | 85.93 |
| ES   |   53498 | 558.1  |   552.42 | 83.74 |
| RS   |  116989 | 559.02 |   552.92 | 83.15 |
| MG   |  298730 | 559.43 |   553.16 | 86.97 |
| SC   |   70312 | 561.87 |   557.06 | 79.15 |
| SP   |  498528 | 562.62 |   558.7  | 83.27 |
| DF   |   54804 | 562.9  |   554.54 | 90.38 |

## Teste: escola privada x pública (participantes)
Diferença de médias: 96.5 pontos (privada 612.7; pública 516.3). t de Welch = 539.26 (p = 0); Mann-Whitney p = 0; d de Cohen = 1.24.

## Média por área e rede
| REDE    |   Ciências da Natureza |   Ciências Humanas |   Linguagens e Códigos |   Matemática |   Redação |
|:--------|-----------------------:|-------------------:|-----------------------:|-------------:|----------:|
| Privada |                  552.8 |              568.7 |                  579.4 |        621.8 |     740.9 |
| Pública |                  480.8 |              494.9 |                  519.2 |        494.1 |     592.4 |

## Redação: média das competências (0 a 200) por rede
| REDE          |   NU_NOTA_COMP1 |   NU_NOTA_COMP2 |   NU_NOTA_COMP3 |   NU_NOTA_COMP4 |   NU_NOTA_COMP5 |
|:--------------|----------------:|----------------:|----------------:|----------------:|----------------:|
| Não informada |           121.6 |           137.5 |           120.5 |           128   |           115.2 |
| Privada       |           137.5 |           157.4 |           139.6 |           153.1 |           153.4 |
| Pública       |           116   |           132.8 |           114.9 |           122   |           106.7 |

## Municípios: estatísticas do perfil socioeconômico e da nota média
|                     |   count |      mean |      std |     min |     25% |     50% |     75% |     max |
|:--------------------|--------:|----------:|---------:|--------:|--------:|--------:|--------:|--------:|
| RENDA_MEDIA_ORD     |    1801 |   2.41658 |  1.14613 |   0.59  |   1.374 |   2.192 |   3.353 |   6.708 |
| PCT_RENDA_ATE_1SM   |    1801 |  52.1261  | 23.8456  |   8.065 |  29.406 |  53.195 |  75.443 |  93.08  |
| PCT_RENDA_ACIMA_5SM |    1801 |   5.52391 |  5.21079 |   0     |   1.327 |   3.76  |   8.653 |  35.184 |
| PCT_MAE_SUPERIOR    |    1801 |  16.4757  |  6.43412 |   2.688 |  11.026 |  15.819 |  21.311 |  43.308 |
| PCT_PAI_SUPERIOR    |    1801 |   8.5351  |  5.1507  |   0.969 |   4.413 |   7.143 |  11.777 |  36.002 |
| PCT_ESCOLA_PRIVADA  |    1801 |  11.3531  | 11.0645  |   0     |   1.852 |   8.252 |  17.869 |  54.922 |
| PCT_WIFI            |    1801 |  85.3159  | 11.9247  |  21.818 |  80.41  |  88.428 |  94.093 |  99.104 |
| PCT_COMPUTADOR      |    1801 |  38.3654  | 17.4991  |   6.696 |  22.121 |  37.069 |  53.868 |  82.418 |
| NOTA_MEDIA          |    1801 | 524.194   | 29.1816  | 441.978 | 503.805 | 523.782 | 545.67  | 608.775 |

## Correlação município: perfil socioeconômico x nota média
- RENDA_MEDIA_ORD: Spearman = 0.81 (p = 0)
- PCT_RENDA_ATE_1SM: Spearman = -0.78 (p = 0)
- PCT_RENDA_ACIMA_5SM: Spearman = 0.80 (p = 0)
- PCT_MAE_SUPERIOR: Spearman = 0.66 (p = 9.78e-224)
- PCT_PAI_SUPERIOR: Spearman = 0.70 (p = 2.17e-269)
- PCT_ESCOLA_PRIVADA: Spearman = 0.73 (p = 4.44e-294)
- PCT_WIFI: Spearman = 0.82 (p = 0)
- PCT_COMPUTADOR: Spearman = 0.85 (p = 0)

Interpretação cautelosa: são associações entre municípios (nível ecológico); não valem automaticamente para indivíduos.

## Média dos municípios por UF
| UF   |   RENDA_MEDIA_ORD |   NOTA_MEDIA |   PCT_ESCOLA_PRIVADA |
|:-----|------------------:|-------------:|---------------------:|
| AM   |              1.25 |       472.02 |                 0.72 |
| AP   |              1.63 |       484.75 |                 3.88 |
| PA   |              1.52 |       489.5  |                 6.43 |
| RR   |              1.93 |       491.78 |                 2.07 |
| AC   |              1.6  |       491.87 |                 1.47 |
| MA   |              1.28 |       492.14 |                 4.65 |
| PI   |              1.24 |       495.76 |                 3.9  |
| TO   |              2.07 |       496.26 |                 4.89 |
| BA   |              1.43 |       506.71 |                 8.93 |
| AL   |              1.48 |       506.82 |                 7.36 |
| SE   |              1.43 |       510.5  |                 7.84 |
| RO   |              2.76 |       513.82 |                 6.17 |
| MS   |              2.93 |       514.16 |                 9.64 |
| MT   |              3.29 |       517.06 |                 9.02 |
| PE   |              1.52 |       520.09 |                 7.37 |
| PB   |              1.44 |       520.56 |                10.53 |
| RN   |              1.75 |       521.99 |                 7.79 |
| CE   |              1.37 |       523.34 |                 3.19 |
| GO   |              2.63 |       525.37 |                 8.47 |
| PR   |              3.61 |       536.62 |                14.63 |
| MG   |              2.8  |       543.17 |                13.65 |
| RJ   |              2.85 |       544.55 |                24.5  |
| ES   |              2.89 |       548.04 |                 9.74 |
| RS   |              3.58 |       550.57 |                13.75 |
| SC   |              4.37 |       552.4  |                18.63 |
| SP   |              3.78 |       555.36 |                25.81 |
| DF   |              4.39 |       562.9  |                30.78 |
