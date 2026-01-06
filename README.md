
# 📊 Dashboard Financeiro

Este projeto é um **dashboard financeiro interativo** desenvolvido em **Python** usando **Streamlit**. Ele permite que o usuário carregue um arquivo CSV com dados financeiros e visualize **métricas, gráficos e relatórios detalhados**.

O dashboard também permite exportar os dados filtrados em **CSV** e gerar um **PDF completo** com gráficos e uma imagem final.

---

## 🚀 Funcionalidades

- Upload de arquivo CSV com dados financeiros.
- Filtro por mês ou exibição de **todos os meses**.
- Métricas principais:
  - Entradas
  - Saídas
  - Saldo
- Gráficos:
  - Entradas x Saídas (barras)
  - Distribuição de gastos por categoria (pizza)
  - Gastos individuais (barras horizontais)
- Tabela detalhada das movimentações.
- Exportação de:
  - CSV do mês filtrado
  - PDF completo com gráficos, tabela e imagem final.

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

