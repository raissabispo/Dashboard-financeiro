
# 📊 Dashboard Financeiro

Este projeto é um **dashboard financeiro interativo** desenvolvido em **Python** usando **Streamlit**. Ele permite que o usuário carregue um arquivo CSV com dados financeiros e visualize **métricas, gráficos e relatórios detalhados**.

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

## 📁 Estrutura do CSV

O arquivo CSV deve conter as seguintes colunas:

| Coluna      | Tipo    | Descrição                            |
|------------|---------|--------------------------------------|
| data       | date    | Data da movimentação (YYYY-MM-DD)    |
| descricao  | string  | Descrição do item                     |
| categoria  | string  | Categoria da movimentação             |
| valor      | float   | Valor da movimentação                 |
| tipo       | string  | "entrada" ou "saida"                  |

**Exemplo de CSV:**

```csv
data,descricao,categoria,valor,tipo
2025-01-05,Salário,Receita,3000,entrada
2025-01-10,Aluguel,Moradia,-1200,saida
2025-01-12,Internet,Serviços,-100,saida
2025-01-15,Freelance,Receita,800,entrada
````

---

## 🎨 Layout

* Paleta de cores **rosa** nos gráficos e barras.
* Dashboard responsivo e interativo.
* Mensagens de alerta quando não há dados ou CSV não foi carregado.

---

## 📄 Exportação de Relatórios

* **CSV:** Exporta os dados do mês filtrado.
* **PDF:** Inclui:

  * Título e resumo financeiro
  * Gráficos (Entradas x Saídas)
  * Tabela detalhada das movimentações
  * Imagem final (`image.png`) abaixo de tudo

---

## 💻 Como rodar

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/dashboard-financeiro.git
```

2. Entre na pasta:

```bash
cd dashboard-financeiro
```

3. Instale as dependências:

```bash
pip install streamlit pandas matplotlib reportlab
```

4. Execute o dashboard:

```bash
streamlit run app.py
```

5. Abra no navegador e faça o upload do CSV ou PDF .



## 🛠 Tecnologias utilizadas

* [Python](https://www.python.org/)
* [Streamlit](https://streamlit.io/)
* [Pandas](https://pandas.pydata.org/)
* [Matplotlib](https://matplotlib.org/)
* [ReportLab](https://www.reportlab.com/)

---

Feito com 💖 por **Raissa Vitória**

```

