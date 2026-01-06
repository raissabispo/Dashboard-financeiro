import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import os

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

# =============================
# Configuração da página
# =============================
st.set_page_config(page_title="Dashboard Financeiro", layout="wide")
st.title("📊 Dashboard Financeiro")

# =============================
# Carregar dados
# =============================
df = pd.read_csv("financeiro.csv")
df["data"] = pd.to_datetime(df["data"])
df["mes"] = df["data"].dt.to_period("M").astype(str)

# =============================
# Função de filtro
# =============================
def filtrar_por_mes(df, mes):
    if mes == "Todos":
        return df
    return df[df["mes"] == mes]

# =============================
# Selectbox
# =============================
lista_meses = ["Todos"] + sorted(df["mes"].unique())
mes_selecionado = st.selectbox("Selecione o mês", lista_meses)

df_mes = filtrar_por_mes(df, mes_selecionado)
titulo_mes = "Todos os meses" if mes_selecionado == "Todos" else mes_selecionado

# =============================
# Métricas
# =============================
total_entradas = df_mes[df_mes["tipo"] == "entrada"]["valor"].sum()
total_saidas = df_mes[df_mes["tipo"] == "saida"]["valor"].sum()
saldo = total_entradas + total_saidas

c1, c2, c3 = st.columns(3)
c1.metric("💰 Entradas", f"R$ {total_entradas:,.2f}")
c2.metric("💸 Saídas", f"R$ {abs(total_saidas):,.2f}")
c3.metric("📌 Saldo", f"R$ {saldo:,.2f}")

# =============================
# Gráfico Entradas x Saídas
# =============================
st.subheader("📈 Entradas x Saídas")

fig_resumo, ax = plt.subplots(figsize=(8, 4))
ax.bar(
    ["Entradas", "Saídas"],
    [total_entradas, abs(total_saidas)],
    color=["#F48FB1", "#F06292"]
)
ax.set_ylabel("Valor (R$)")
ax.set_title(f"Resumo Financeiro — {titulo_mes}")
st.pyplot(fig_resumo)

# =============================
# Gráfico Pizza por Categoria
# =============================
st.subheader("🍕 Gastos por Categoria")

gastos_categoria = (
    df_mes[df_mes["tipo"] == "saida"]
    .groupby("categoria")["valor"]
    .sum()
    .abs()
)

if not gastos_categoria.empty:
    fig_pizza, ax_pizza = plt.subplots()
    ax_pizza.pie(
        gastos_categoria,
        labels=gastos_categoria.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=["#F8BBD0", "#F48FB1", "#F06292", "#EC407A"]
    )
    ax_pizza.set_title("Distribuição de Gastos")
    st.pyplot(fig_pizza)
else:
    st.info("Não há gastos por categoria.")

# =============================
# Gráfico Gastos Individuais
# =============================
st.subheader("📉 Gastos Individuais")

gastos_individuais = df_mes[df_mes["tipo"] == "saida"].sort_values("valor")

if not gastos_individuais.empty:
    fig_gastos, ax_gastos = plt.subplots(figsize=(10, 4))
    ax_gastos.barh(
        gastos_individuais["descricao"],
        gastos_individuais["valor"].abs(),
        color="#F06292"
    )
    ax_gastos.set_xlabel("Valor (R$)")
    ax_gastos.set_title("Gastos Individuais")
    st.pyplot(fig_gastos)
else:
    st.info("Não há gastos registrados.")

# =============================
# Tabela
# =============================
st.subheader("📋 Detalhamento")
st.dataframe(df_mes, use_container_width=True)

# =============================
# Exportar CSV
# =============================
st.download_button(
    label="⬇️ Exportar CSV",
    data=df_mes.to_csv(index=False),
    file_name=f"financeiro_{titulo_mes}.csv",
    mime="text/csv"
)

# =============================
# Função PDF
# =============================
def gerar_pdf(df_pdf, titulo, entradas, saidas, saldo, fig):
    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=A4)
    estilos = getSampleStyleSheet()
    elementos = []

    elementos.append(Paragraph(f"Relatório Financeiro — {titulo}", estilos["Title"]))
    elementos.append(Spacer(1, 12))

    resumo = Table([
        ["Entradas", f"R$ {entradas:,.2f}"],
        ["Saídas", f"R$ {abs(saidas):,.2f}"],
        ["Saldo", f"R$ {saldo:,.2f}"],
    ])

    resumo.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 1, colors.pink),
        ("BACKGROUND", (0,0), (-1,0), colors.lightpink),
    ]))

    elementos.append(resumo)
    elementos.append(Spacer(1, 16))

    # Gráfico
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format="png", bbox_inches="tight")
    img_buffer.seek(0)
    elementos.append(Image(img_buffer, width=400, height=250))
    elementos.append(Spacer(1, 16))

    # Tabela
    dados = [["Data", "Descrição", "Categoria", "Tipo", "Valor"]]
    for _, row in df_pdf.iterrows():
        dados.append([
            row["data"].strftime("%d/%m/%Y"),
            row["descricao"],
            row["categoria"],
            row["tipo"],
            f"R$ {row['valor']:,.2f}"
        ])

    tabela = Table(dados, repeatRows=1)
    tabela.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.5, colors.pink),
        ("BACKGROUND", (0,0), (-1,0), colors.lightpink),
    ]))

    elementos.append(tabela)
    elementos.append(Spacer(1, 24))

    # IMAGEM FINAL
    if os.path.exists("image.png"):
        elementos.append(Image("image.png", width=200, height=200))
        elementos.append(Spacer(1, 12))

    pdf.build(elementos)
    buffer.seek(0)
    return buffer

# =============================
# Botão PDF
# =============================
pdf = gerar_pdf(
    df_mes,
    titulo_mes,
    total_entradas,
    total_saidas,
    saldo,
    fig_resumo
)

st.download_button(
    label="📄 Exportar PDF",
    data=pdf,
    file_name=f"relatorio_financeiro_{titulo_mes}.pdf",
    mime="application/pdf"
)
