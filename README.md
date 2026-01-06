
# 📊 Dashboard Financeiro com Streamlit

Este projeto é um **Dashboard Financeiro interativo**, desenvolvido em **Python com Streamlit**, que permite visualizar, analisar e exportar dados financeiros de forma simples e visual.

---

## 🚀 Funcionalidades

- 📅 **Filtro por mês** (incluindo opção *Todos os meses*)
- 💰 **Métricas financeiras**:
  - Total de entradas
  - Total de saídas
  - Saldo final
- 📈 **Gráfico de barras** (Entradas x Saídas)
- 🍕 **Gráfico de pizza** (Gastos por categoria)
- 📉 **Gráfico de gastos individuais**
- 📋 **Tabela detalhada das movimentações**
- ⬇️ **Exportação dos dados em CSV**
- 📄 **Exportação de relatório em PDF**, contendo:
  - Resumo financeiro
  - Gráfico
  - Tabela detalhada
  - Imagem final personalizada (`image.png`)
- 🎨 **Paleta de cores rosa** em todo o dashboard

---

## 🛠️ Tecnologias Utilizadas

- **Python**
- **Streamlit**
- **Pandas**
- **Matplotlib**
- **ReportLab** (geração de PDF)

---

## 📁 Estrutura do Projeto

```text
projeto/
├── app.py
├── financeiro.csv (deve substituir por outro csv)
├── image.png
├── requirements.txt
└── README.md
````

---

## 📄 Estrutura do arquivo `financeiro.csv`

O arquivo CSV deve conter as seguintes colunas:

```
data,descricao,categoria,tipo,valor
```

### Exemplo:

```csv
2024-01-05,Salário,Receita,entrada,3000
2024-01-10,Aluguel,Moradia,saida,-1200
2024-01-15,Supermercado,Alimentação,saida,-450
```

> ⚠️ Importante:
>
> * O campo **tipo** deve ser `entrada` ou `saida`
> * Os valores de **saída** devem ser negativos

---

## ▶️ Como Executar o Projeto Localmente

### 1️⃣ Clone o repositório

```bash
git clone https://github.com/seu-usuario/dashboard-financeiro.git
```

### 2️⃣ Acesse a pasta

```bash
cd dashboard-financeiro
```

### 3️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Execute a aplicação

```bash
streamlit run app.py
```

---


## 👩‍💻 Autora

**Raissa Vitória**
Estudante de Análise e Desenvolvimento de Sistemas
Apaixonada por tecnologia, dados e soluções inteligentes 💗

