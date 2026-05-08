# =========================================
# DASHBOARD FINANCEIRO COMPLETO
# =========================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import os

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

# =========================================
# CONFIGURAÇÃO
# =========================================

st.set_page_config(
    page_title="Dashboard Financeiro",
    layout="wide"
)

st.title("📊 Dashboard Financeiro")

# =========================================
# SESSION STATE
# =========================================

if "dados" not in st.session_state:
    st.session_state.dados = []

# =========================================
# IMPORTAR CSV
# =========================================

st.subheader("📁 Importar CSV")

arquivo = st.file_uploader(
    "Selecione um CSV",
    type=["csv"]
)

if arquivo is not None:

    try:

        df_csv = pd.read_csv(
            arquivo,
            sep=";"
        )

        df_csv.columns = (
            df_csv.columns
            .str.strip()
            .str.lower()
        )

        # remover coluna mes
        if "mes" in df_csv.columns:

            df_csv = df_csv.drop(
                columns=["mes"]
            )

        colunas_necessarias = [
            "data",
            "descricao",
            "categoria",
            "valor",
            "tipo"
        ]

        if all(
            coluna in df_csv.columns
            for coluna in colunas_necessarias
        ):

            df_csv["data"] = pd.to_datetime(
                df_csv["data"],
                errors="coerce"
            )

            df_csv = df_csv.dropna(
                subset=["data"]
            )

            if "csv_importado" not in st.session_state:

                for _, row in df_csv.iterrows():

                    novo = {
                        "data": row["data"],
                        "descricao": row["descricao"],
                        "categoria": row["categoria"],
                        "valor": float(row["valor"]),
                        "tipo": row["tipo"]
                    }

                    st.session_state.dados.append(
                        novo
                    )

                st.session_state.csv_importado = True

                st.success(
                    "✅ CSV importado com sucesso!"
                )

        else:

            st.error(
                "❌ CSV precisa conter:\n"
                "data, descricao, categoria, valor, tipo"
            )

    except Exception as e:

        st.error(
            f"Erro ao importar CSV: {e}"
        )

# =========================================
# FORMULÁRIO
# =========================================

st.subheader("➕ Adicionar movimentação")

with st.form("form_movimentacao"):

    col1, col2 = st.columns(2)

    with col1:

        data = st.date_input("📅 Data")

        descricao = st.text_input(
            "📝 Descrição"
        )

        categoria = st.text_input(
            "🏷️ Categoria"
        )

    with col2:

        valor = st.number_input(
            "💰 Valor",
            min_value=0.0,
            step=0.01
        )

        tipo = st.selectbox(
            "📌 Tipo",
            ["entrada", "saida"]
        )

    submitted = st.form_submit_button(
        "Adicionar movimentação"
    )

# =========================================
# ADICIONAR
# =========================================

if submitted:

    valor_final = valor

    if tipo == "saida":
        valor_final = -abs(valor)

    novo = {
        "data": data,
        "descricao": descricao,
        "categoria": categoria,
        "valor": valor_final,
        "tipo": tipo
    }

    st.session_state.dados.append(
        novo
    )

    st.success(
        "✅ Movimentação adicionada!"
    )

# =========================================
# PROCESSAR DADOS
# =========================================

if len(st.session_state.dados) > 0:

    df = pd.DataFrame(
        st.session_state.dados
    )

    df["data"] = pd.to_datetime(
        df["data"]
    )

    # =====================================
    # NOME DO MÊS
    # =====================================

    primeira_data = pd.to_datetime(
        df["data"].iloc[0]
    )

    meses_pt = {
        1: "Janeiro",
        2: "Fevereiro",
        3: "Março",
        4: "Abril",
        5: "Maio",
        6: "Junho",
        7: "Julho",
        8: "Agosto",
        9: "Setembro",
        10: "Outubro",
        11: "Novembro",
        12: "Dezembro"
    }

    nome_mes = (
        f"{meses_pt[primeira_data.month]} "
        f"de {primeira_data.year}"
    )

    # =====================================
    # MÉTRICAS
    # =====================================

    total_entradas = (
        df[df["tipo"] == "entrada"]
        ["valor"]
        .sum()
    )

    total_saidas = (
        df[df["tipo"] == "saida"]
        ["valor"]
        .sum()
    )

    saldo = (
        total_entradas +
        total_saidas
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "💰 Entradas",
        f"R$ {total_entradas:,.2f}"
    )

    c2.metric(
        "💸 Saídas",
        f"R$ {abs(total_saidas):,.2f}"
    )

    c3.metric(
        "📌 Saldo",
        f"R$ {saldo:,.2f}"
    )

    # =====================================
    # GRÁFICO RESUMO
    # =====================================

    fig_resumo, ax = plt.subplots(
        figsize=(7, 4)
    )

    ax.bar(
        ["Entradas", "Saídas"],
        [total_entradas, abs(total_saidas)],
        color=["#F48FB1", "#F06292"]
    )

    ax.set_ylabel(
        "Valor (R$)"
    )

    ax.set_title(
        f"Resumo Financeiro — {nome_mes}"
    )

    st.pyplot(fig_resumo)

    # =====================================
    # DONUT
    # =====================================

    gastos_categoria = (
        df[df["tipo"] == "saida"]
        .groupby("categoria")["valor"]
        .sum()
        .abs()
    )

    fig_donut = None

    if not gastos_categoria.empty:

        fig_donut, ax_donut = plt.subplots(
            figsize=(8, 8)
        )

        cores = [
            "#FFB6C1",
            "#FF69B4",
            "#FF1493",
            "#DB7093",
            "#C71585",
            "#DA70D6",
            "#BA55D3"
        ]

        explode = [0.03] * len(
            gastos_categoria
        )

        wedges, texts, autotexts = (
            ax_donut.pie(
                gastos_categoria.values,
                autopct="%1.1f%%",
                startangle=90,
                colors=cores[
                    :len(gastos_categoria)
                ],
                explode=explode,
                wedgeprops=dict(
                    width=0.45,
                    edgecolor="white"
                )
            )
        )

        centro = plt.Circle(
            (0, 0),
            0.25,
            fc="white"
        )

        ax_donut.add_artist(
            centro
        )

        total_gastos = (
            gastos_categoria.sum()
        )

        ax_donut.text(
            0,
            0,
            f"R$ {total_gastos:,.2f}",
            ha="center",
            va="center",
            fontsize=14,
            fontweight="bold"
        )

        ax_donut.legend(
            wedges,
            gastos_categoria.index,
            title="Categorias",
            loc="center left",
            bbox_to_anchor=(1, 0.5)
        )

        ax_donut.set_title(
            "Distribuição de Gastos"
        )

        st.pyplot(fig_donut)

    # =====================================
    # GASTOS INDIVIDUAIS
    # =====================================

    gastos_individuais = (
        df[df["tipo"] == "saida"]
        .sort_values("valor")
    )

    fig_gastos = None

    if not gastos_individuais.empty:

        fig_gastos, ax_gastos = (
            plt.subplots(
                figsize=(10, 5)
            )
        )

        ax_gastos.barh(
            gastos_individuais[
                "descricao"
            ],
            gastos_individuais[
                "valor"
            ].abs(),
            color="#F06292"
        )

        ax_gastos.set_xlabel(
            "Valor (R$)"
        )

        ax_gastos.set_title(
            "Gastos Individuais"
        )

        st.pyplot(fig_gastos)

    # =====================================
    # TABELA
    # =====================================

    st.subheader("📋 Detalhamento")

    st.dataframe(
        df,
        use_container_width=True
    )

    # =====================================
    # EXCLUIR
    # =====================================

    st.subheader(
        "🗑️ Excluir movimentação"
    )

    for i, row in (
        df.reset_index()
        .iterrows()
    ):

        col1, col2, col3, col4 = (
            st.columns([2, 3, 2, 1])
        )

        with col1:

            st.write(
                row["data"]
                .strftime("%d/%m/%Y")
            )

        with col2:

            st.write(
                row["descricao"]
            )

        with col3:

            st.write(
                f"R$ {row['valor']:,.2f}"
            )

        with col4:

            if st.button(
                "❌",
                key=f"delete_{i}"
            ):

                st.session_state.dados.pop(
                    row["index"]
                )

                st.rerun()

    # =====================================
    # EXPORTAR CSV
    # =====================================

    df_exportar = df.copy()

    df_exportar["data"] = (
        pd.to_datetime(
            df_exportar["data"]
        )
        .dt.strftime("%Y-%m-%d")
    )

    csv = df_exportar.to_csv(
        index=False,
        sep=";",
        encoding="utf-8-sig"
    )

    st.download_button(
        label="⬇️ Exportar CSV",
        data=csv,
        file_name="financeiro.csv",
        mime="text/csv"
    )

    # =====================================
    # PDF
    # =====================================

    def gerar_pdf():

        buffer = io.BytesIO()

        pdf = SimpleDocTemplate(
            buffer,
            pagesize=A4
        )

        estilos = (
            getSampleStyleSheet()
        )

        elementos = []

        elementos.append(
            Paragraph(
                f"""
                Relatório Financeiro<br/>
                {nome_mes}
                """,
                estilos["Title"]
            )
        )

        elementos.append(
            Spacer(1, 20)
        )

        resumo = Table([
            [
                "Entradas",
                f"R$ {total_entradas:,.2f}"
            ],
            [
                "Saídas",
                f"R$ {abs(total_saidas):,.2f}"
            ],
            [
                "Saldo",
                f"R$ {saldo:,.2f}"
            ]
        ])

        resumo.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.pink
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.black
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, -1),
                    "Helvetica-Bold"
                ),
                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER"
                )
            ])
        )

        elementos.append(resumo)

        elementos.append(
            Spacer(1, 20)
        )

        for fig in [
            fig_resumo,
            fig_donut,
            fig_gastos
        ]:

            if fig is not None:

                img_buffer = io.BytesIO()

                fig.savefig(
                    img_buffer,
                    format="png",
                    bbox_inches="tight"
                )

                img_buffer.seek(0)

                elementos.append(
                    Image(
                        img_buffer,
                        width=450,
                        height=250
                    )
                )

                elementos.append(
                    Spacer(1, 20)
                )

        dados = [[
            "Data",
            "Descrição",
            "Categoria",
            "Tipo",
            "Valor"
        ]]

        for _, row in (
            df.iterrows()
        ):

            dados.append([
                row["data"]
                .strftime("%d/%m/%Y"),
                row["descricao"],
                row["categoria"],
                row["tipo"],
                f"R$ {row['valor']:,.2f}"
            ])

        tabela = Table(dados)

        tabela.setStyle(
            TableStyle([
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.black
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightpink
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER"
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    9
                )
            ])
        )

        elementos.append(
            Spacer(1, 20)
        )

        elementos.append(tabela)

        # =================================
        # IMAGE.PNG
        # =================================

        if os.path.exists("image.png"):

            elementos.append(
                Spacer(1, 30)
            )

            elementos.append(
                Image(
                    "image.png",
                    width=450,
                    height=250
                )
            )

        pdf.build(elementos)

        buffer.seek(0)

        return buffer

    pdf_buffer = gerar_pdf()

    st.download_button(
        "📄 Exportar PDF",
        pdf_buffer,
        file_name="relatorio_financeiro.pdf",
        mime="application/pdf"
    )

else:

    st.info(
        "Adicione movimentações ou importe um CSV."
    )