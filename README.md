# Analisador de Vendas

Projeto de Engenharia de Dados desenvolvido em Python para simular um pipeline de processamento e análise de vendas de uma loja fictícia de acessórios de informática.

O projeto implementa um fluxo ETL (Extract, Transform, Load), contemplando extração de dados CSV, validação, transformação, persistência em banco de dados relacional, análises SQL e geração de visualizações.

## Objetivos

- Praticar conceitos de Engenharia de Dados.
- Desenvolver um pipeline ETL organizado e automatizado.
- Implementar validação e tratamento de dados inconsistentes.
- Trabalhar com persistência e modelagem relacional utilizando SQLite.
- Desenvolver consultas SQL para análise de indicadores de negócio.
- Aplicar verificações de integridade e prevenção de duplicidades.

## Tecnologias utilizadas

- Python
- SQLite
- SQL
- CSV e JSON
- Matplotlib
- Unittest
- Git e GitHub

## Arquitetura do pipeline

O projeto é organizado nas seguintes etapas:

1. **Extração:** leitura dos dados brutos a partir de um arquivo CSV.
2. **Validação:** identificação de registros inválidos e separação dos dados rejeitados.
3. **Transformação:** limpeza, padronização e organização dos registros válidos.
4. **Carga:** persistência dos dados em um banco SQLite, com relacionamento entre produtos e vendas.
5. **Integridade:** reconciliação dos dados processados com os registros armazenados no banco.
6. **Relatórios:** geração de indicadores e análises utilizando Python e SQL.
7. **Visualização:** geração de gráficos para análise do faturamento.

## Estrutura do projeto

```text
analisador-vendas/
├── data/
│   ├── raw/
│   └── processed/
│       └── charts/
├── database/
├── logs/
├── src/
│   ├── extract_sales.py
│   ├── validation.py
│   ├── validate_sales.py
│   ├── transform_sales.py
│   ├── generate_report.py
│   ├── database.py
│   ├── init_database.py
│   ├── repository.py
│   ├── load_database.py
│   ├── analytics.py
│   ├── generate_analytics_report.py
│   ├── integrity_check.py
│   ├── visualize_data.py
│   ├── logger.py
│   └── run_pipeline.py
├── requirements.txt
└── README.md
```

## Funcionalidades

### Qualidade dos dados

- Validação de campos obrigatórios.
- Verificação de datas, quantidades e valores monetários.
- Identificação de registros inconsistentes.
- Separação dos registros rejeitados para análise posterior.

### Banco de dados

- Modelagem relacional com tabelas de produtos e vendas.
- Relacionamento por chaves primárias e estrangeiras.
- Prevenção de registros duplicados.
- Armazenamento monetário em centavos inteiros.
- Persistência utilizando SQLite.

### Análises SQL

- Faturamento por produto.
- Quantidade de unidades vendidas por produto.
- Faturamento mensal.
- Produto com maior faturamento.
- Participação percentual dos produtos no faturamento.
- Indicadores gerais de vendas.

### Integridade dos dados

Comparação entre os dados processados em CSV e os dados persistidos no SQLite, verificando quantidade de vendas, produtos, unidades e faturamento.

### Visualizações

Geração de gráficos utilizando Matplotlib:

- Faturamento por produto.
- Evolução do faturamento mensal.

## Como executar

### 1. Pré-requisitos

- Python instalado.
- pip.

### 2. Instalar dependências

```bash
python -m pip install -r requirements.txt
```

### 3. Inicializar o banco de dados

```bash
python src/init_database.py
```

### 4. Executar o pipeline

```bash
python src/run_pipeline.py
```

O pipeline executará automaticamente todas as etapas, desde a extração dos dados até a geração dos relatórios e gráficos.

## Resultados

O projeto utiliza uma base fictícia contendo registros de vendas, incluindo exemplos de dados inconsistentes para demonstrar as etapas de validação e tratamento.

Indicadores obtidos na base utilizada durante o desenvolvimento:

| Indicador | Resultado |
|---|---:|
| Registros recebidos | 18 |
| Registros válidos | 15 |
| Registros rejeitados | 3 |
| Produtos cadastrados | 5 |
| Unidades vendidas | 39 |
| Faturamento total | R$ 7.283,10 |
| Ticket médio | R$ 485,54 |

Os resultados são armazenados em relatórios JSON e gráficos PNG dentro do diretório `data/processed/`.

## Aprendizados

Durante o desenvolvimento, foram praticados conceitos de:

- Construção de pipelines ETL.
- Qualidade e validação de dados.
- Manipulação de arquivos CSV e JSON.
- Modelagem e persistência relacional.
- Consultas SQL e agregações.
- Integridade e reconciliação de dados.
- Automação de processos com Python.
- Logging e tratamento de erros.
- Visualização e análise de dados.

---

Projeto desenvolvido para fins de aprendizado e prática de Engenharia de Dados.