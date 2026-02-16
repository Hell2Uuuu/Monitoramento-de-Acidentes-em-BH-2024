# 🚦 Monitoramento de Acidentes de Trânsito em BH (2024)

![Dashboard Preview](images/DashBoard.png)
> *Visão geral do Dashboard interativo construído no Power BI.*

## 📋 Sobre o Projeto

Este projeto consiste em uma análise de dados ponta-a-ponta (End-to-End) sobre a segurança viária em Belo Horizonte/MG. Utilizando dados abertos da Prefeitura (PBH), o objetivo foi mapear padrões de acidentes, identificar gargalos de trânsito e horários críticos para auxiliar na tomada de decisão.

O principal desafio técnico foi o **tratamento de dados geoespaciais**, exigindo a conversão de coordenadas planas (UTM) para geográficas (Latitude/Longitude) via Python para plotagem precisa no mapa.

## 🛠️ Tecnologias Utilizadas

* **Python 3.12**: Linguagem principal para ETL.
    * `Pandas`: Limpeza, manipulação e engenharia de atributos (extração de datas/horas).
    * `PyProj`: Biblioteca para conversão de sistemas de coordenadas (SIRGAS 2000 -> WGS84).
* **Excel**: Armazenamento intermediário dos dados estruturados.
* **Power BI**: Construção do Dashboard interativo, medidas DAX e visualização de dados.
* **Git/GitHub**: Controle de versão e documentação.

## 📊 Principais Insights

Com base na análise de **[Inserir total de acidentes, ex: 12.561]** ocorrências em 2024, identificou-se que:

1.  **Horário de Pico:** O momento mais crítico do trânsito é às **18h**, com foco nas **Sextas-feiras**, indicando forte correlação com a saída do trabalho/happy hour.
2.  **Pontos Críticos:** A regional **[Inserir Regional, ex: Centro-Sul]** concentra o maior volume de ocorrências.
3.  **Tipologia:** Acidentes do tipo **[Inserir tipo, ex: Colisão]** representam a maioria dos casos registrados.

## 🗂️ Estrutura do Projeto

```bash
├── data/
│   ├── raw/                   # Dados brutos (CSV original da PBH)
│   └── processed/             # Dados tratados (Excel com Lat/Long corrigidas)
├── src/
│   └── etl_acidentes.py       # Script Python de tratamento de dados
├── dashboard/
│   └── dashboard_mobilidade.pbix  # Arquivo do Power BI
├── images/
│   └── dashboard_print.png    # Imagens para documentação
└── README.md
