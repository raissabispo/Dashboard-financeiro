import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

# -----------------------------
st.set_page_config(page_title="Dashboard Financeiro", layout="wide")
st.title("📊 Dashboard Financeiro")

# -----------------------------
# Upload CSV
arquivo = st.file_uploader("📁 Faça upload do seu arquivo CSV", type=["csv"])

if arquivo is not None:
    try:
        df = pd.read_csv(arquivo)
    except Exception as e:
        st.error(f"Erro ao ler o CSV: {e}")
        st.stop()

    # Converter coluna de data e criar coluna de mês
    try:
        df["data"] = pd.to_datetime(df["data"])
        df["mes"] = df["data"].dt.to_period("M").astype(str)
    except Exception as e:
        st.error(f"Erro ao processar datas: {e}")
        st.stop()

    # -----------------------------
    # Filtro por mês
    lista_meses = ["Todos"] + sorted(df["mes"].unique())
    mes_selecionado = st.selectbox("Selecione o mês", lista_meses)

    df_mes = df if mes_selecionado == "Todos" else df[df["mes"] == mes_selecionado]
    titulo_mes = "Todos os meses" if mes_selecionado == "Todos" else mes_selecionado

    # -----------------------------
    # Métricas
    total_entradas = df_mes[df_mes["tipo"] == "entrada"]["valor"].sum()
    total_saidas = df_mes[df_mes["tipo"] == "saida"]["valor"].sum()
    saldo = total_entradas + total_saidas

    c1, c2, c3 = st.columns(3)
    c1.metric("💰 Entradas", f"R$ {total_entradas:,.2f}")
    c2.metric("💸 Saídas", f"R$ {abs(total_saidas):,.2f}")
    c3.metric("📌 Saldo", f"R$ {saldo:,.2f}")

    # ==================================================
    # GRÁFICOS
    # ==================================================
    # Entradas x Saídas
    fig_resumo, ax = plt.subplots(figsize=(8, 4))
    ax.bar(["Entradas", "Saídas"], [total_entradas, abs(total_saidas)], color=["#F48FB1", "#F06292"])
    ax.set_ylabel("Valor (R$)")
    ax.set_title(f"Resumo Financeiro — {titulo_mes}")
    st.pyplot(fig_resumo)

    # Gráfico de Donut por categoria
    gastos_categoria = df_mes[df_mes["tipo"] == "saida"].groupby("categoria")["valor"].sum().abs()
    fig_donut = None
    if not gastos_categoria.empty:
        fig_donut, ax_donut = plt.subplots(figsize=(10, 8))
        
        # Ordenar por valor (do maior para o menor)
        gastos_categoria = gastos_categoria.sort_values(ascending=False)
        
        # Paleta de cores rosa/vermelho
        cores = [
            "#FFB6C1", "#FF69B4", "#FF1493", "#DB7093", "#C71585",
            "#DA70D6", "#BA55D3", "#9932CC", "#8A2BE2", "#9370DB"
        ]
        
        # Adicionar um pouco de separação entre as fatias
        explode = [0.05] * len(gastos_categoria)
        
        # Criar donut chart
        wedges, texts, autotexts = ax_donut.pie(
            gastos_categoria.values,
            labels=None,  # Removemos labels para colocar na legenda
            autopct=lambda pct: f"{pct:.1f}%" if pct >= 5 else "",
            startangle=90,
            colors=cores[:len(gastos_categoria)],
            wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2),
            explode=explode,
            pctdistance=0.75,
            textprops={'fontsize': 10, 'fontweight': 'bold', 'color': 'white'}
        )
        
        # Adicionar círculo branco no centro para criar o efeito donut
        centro_circulo = plt.Circle((0, 0), 0.25, fc='white', edgecolor='white', linewidth=2)
        ax_donut.add_artist(centro_circulo)
        
        # Adicionar título no centro
        total_gastos = gastos_categoria.sum()
        ax_donut.text(0, 0.1, f'TOTAL', 
                     ha='center', va='center', 
                     fontsize=14, fontweight='bold', color='#333333')
        ax_donut.text(0, -0.05, f'R$ {total_gastos:,.2f}', 
                     ha='center', va='center', 
                     fontsize=16, fontweight='bold', color='#FF1493')
        
        # Criar legenda detalhada
        legend_labels = []
        for cat, val in gastos_categoria.items():
            porcentagem = (val / total_gastos) * 100
            legend_labels.append(f"{cat}: R$ {val:,.2f} ({porcentagem:.1f}%)")
        
        # Adicionar legenda fora do gráfico
        ax_donut.legend(
            wedges, 
            legend_labels,
            title="Categorias de Gastos",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1),
            fontsize=10,
            title_fontsize=12
        )
        
        ax_donut.set_title(f"Distribuição de Gastos por Categoria — {titulo_mes}", 
                          fontsize=16, fontweight='bold', pad=20, color='#333333')
        ax_donut.set_aspect('equal')  # Garantir que o gráfico seja circular
        
        # Ajustar layout para caber a legenda
        plt.tight_layout()
        st.pyplot(fig_donut)
        
        # Mostrar tabela de categorias para referência
        with st.expander("📊 Ver detalhes por categoria"):
            gastos_df = gastos_categoria.reset_index()
            
            # Verificar o nome real das colunas
            if len(gastos_df.columns) == 2:
                # Renomear colunas de forma segura
                gastos_df.columns = ['Categoria', 'Valor_Total']
                
                # Calcular porcentagem
                gastos_df['Porcentagem'] = (gastos_df['Valor_Total'] / total_gastos * 100).round(1)
                
                gastos_df = gastos_df.sort_values('Valor_Total', ascending=False)
                st.dataframe(gastos_df, use_container_width=True)
            else:
                st.write("Erro: Estrutura de dados inesperada")

    # Gastos individuais
    gastos_individuais = df_mes[df_mes["tipo"] == "saida"].sort_values("valor")
    fig_gastos = None
    if not gastos_individuais.empty:
        fig_gastos, ax_gastos = plt.subplots(figsize=(10, 4))
        ax_gastos.barh(gastos_individuais["descricao"], gastos_individuais["valor"].abs(), color="#F06292")
        ax_gastos.set_xlabel("Valor (R$)")
        ax_gastos.set_title(f"Gastos Individuais — {titulo_mes}")
        st.pyplot(fig_gastos)

    # -----------------------------
    # Tabela de dados
    st.subheader("📋 Detalhamento")
    st.dataframe(df_mes, use_container_width=True)

    # -----------------------------
    # Exportar CSV
    st.download_button(
        "⬇️ Exportar CSV",
        df_mes.to_csv(index=False),
        file_name=f"financeiro_{titulo_mes}.csv",
        mime="text/csv"
    )

    # -----------------------------
    # VERIFICAR SE O ARQUIVO IMAGE.PNG EXISTE
    def verificar_imagem_final():
        """Verifica se o arquivo image.png existe na raiz do projeto"""
        caminhos_possiveis = [
            "image.png",  # Raiz do projeto
            "./image.png",
            os.path.join(os.path.dirname(__file__), "image.png"),
            os.path.join(os.getcwd(), "image.png")
        ]
        
        for caminho in caminhos_possiveis:
            if os.path.exists(caminho):
                st.success(f"✅ Imagem encontrada: {caminho}")
                return caminho
        
        # Se não encontrar, criar uma imagem temporária
        st.warning("⚠️ Arquivo image.png não encontrado. Criando imagem temporária...")
        return criar_imagem_temporaria()

    def criar_imagem_temporaria():
        """Cria uma imagem temporária se image.png não existir"""
        fig, ax = plt.subplots(figsize=(10, 4))
        
        # Criar design da imagem temporária
        ax.text(0.5, 0.7, "📊 Dashboard Financeiro", 
                ha='center', va='center', fontsize=20, fontweight='bold', color='#FF1493')
        ax.text(0.5, 0.5, "Relatório Gerado Automaticamente", 
                ha='center', va='center', fontsize=14, color='#333333')
        ax.text(0.5, 0.3, f"Período: {titulo_mes}", 
                ha='center', va='center', fontsize=12, color='#666666')
        
        # Adicionar informações
        from datetime import datetime
        data_atual = datetime.now().strftime("%d/%m/%Y")
        ax.text(0.5, 0.1, f"Data: {data_atual}", 
                ha='center', va='center', fontsize=10, color='#999999')
        
        # Remover eixos
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        # Salvar temporariamente
        import tempfile
        temp_path = os.path.join(tempfile.gettempdir(), "image_temp.png")
        fig.savefig(temp_path, format='png', dpi=150, bbox_inches='tight', facecolor='#F8F8F8')
        plt.close(fig)
        
        return temp_path

    # Verificar imagem
    caminho_imagem = verificar_imagem_final()

    # -----------------------------
    # FUNÇÃO PARA GERAR PDF COM IMAGEM FINAL
    def gerar_pdf(df_pdf, titulo, entradas, saidas, saldo, figs, imagem_path):
        buffer = io.BytesIO()
        pdf = SimpleDocTemplate(buffer, pagesize=A4)
        estilos = getSampleStyleSheet()
        elementos = []

        # Título
        elementos.append(Paragraph(f"Relatório Financeiro — {titulo}", estilos["Title"]))
        elementos.append(Spacer(1, 12))

        # Resumo financeiro
        elementos.append(Paragraph("Resumo Financeiro", estilos["Heading2"]))
        elementos.append(Spacer(1, 8))
        
        resumo = Table(
            [["Entradas", f"R$ {entradas:,.2f}"],
             ["Saídas", f"R$ {abs(saidas):,.2f}"],
             ["Saldo", f"R$ {saldo:,.2f}"]],
            colWidths=[200, 200]
        )
        resumo.setStyle(TableStyle([
            ("GRID", (0,0), (-1,-1), 1, colors.black),
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#F48FB1")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("FONTSIZE", (0,0), (-1,-1), 12),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold")
        ]))
        elementos.append(resumo)
        elementos.append(Spacer(1, 24))

        # Adicionar todos os gráficos
        elementos.append(Paragraph("Visualizações Gráficas", estilos["Heading2"]))
        elementos.append(Spacer(1, 12))
        
        for fig in figs:
            if fig is not None:
                img_buf = io.BytesIO()
                fig.savefig(img_buf, format="png", bbox_inches="tight", dpi=150)
                plt.close(fig)
                img_buf.seek(0)
                try:
                    elementos.append(Image(img_buf, width=500, height=300))
                    elementos.append(Spacer(1, 20))
                except (OSError, ValueError) as e:
                    st.warning(f"Erro ao adicionar gráfico ao PDF: {e}")

        # Detalhamento
        elementos.append(Paragraph("Detalhamento das Movimentações", estilos["Heading2"]))
        elementos.append(Spacer(1, 12))
        elementos.append(Paragraph(f"Total de registros: {len(df_pdf)}", estilos["Normal"]))
        elementos.append(Spacer(1, 8))
        
        dados = [["Data", "Descrição", "Categoria", "Tipo", "Valor (R$)"]]
        for _, row in df_pdf.iterrows():
            # Formatar tipo com cores
            tipo = row["tipo"]
            valor_formatado = f"R$ {row['valor']:,.2f}"
            
            dados.append([
                row["data"].strftime("%d/%m/%Y"), 
                row["descricao"][:30] + "..." if len(row["descricao"]) > 30 else row["descricao"], 
                row["categoria"], 
                tipo,
                valor_formatado
            ])
        
        tabela = Table(dados, repeatRows=1, colWidths=[80, 150, 80, 60, 80])
        
        # CORREÇÃO: Remover as referências à variável 'table' que não existe
        # Em vez disso, vamos acessar os dados diretamente do df_pdf
        tabela.setStyle(TableStyle([
            ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#F0F0F0")),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("ALIGN", (1,1), (1,-1), "LEFT"),  # Alinhar descrição à esquerda
            ("FONTSIZE", (0,0), (-1,-1), 9),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F8F8F8")]),
        ]))
        
        # Adicionar cores condicionais para tipo e valor
        # Percorrer as linhas e aplicar cores baseadas nos dados
        for i, row in enumerate(df_pdf.iterrows(), start=1):  # start=1 porque a linha 0 é o cabeçalho
            _, data_row = row
            if data_row["tipo"] == "saida":
                # Aplicar cor vermelha para saídas
                tabela.setStyle(TableStyle([
                    ("TEXTCOLOR", (3, i), (3, i), colors.red),  # Coluna Tipo
                    ("TEXTCOLOR", (4, i), (4, i), colors.red),  # Coluna Valor
                ]))
            else:
                # Aplicar cor verde para entradas
                tabela.setStyle(TableStyle([
                    ("TEXTCOLOR", (3, i), (3, i), colors.green),  # Coluna Tipo
                    ("TEXTCOLOR", (4, i), (4, i), colors.green),  # Coluna Valor
                ]))
        
        elementos.append(tabela)
        elementos.append(Spacer(1, 24))

        # IMAGEM FINAL DO ARQUIVO image.png
        elementos.append(Spacer(1, 12))
        
        # Adicionar a imagem do arquivo image.png
        try:
            # Verificar se o arquivo existe e é válido
            if os.path.exists(imagem_path):
                # Adicionar imagem com tamanho ajustado
                img_final = Image(imagem_path, width=500, height=300)
                elementos.append(img_final)
                elementos.append(Spacer(1, 12))
                
                # Adicionar legenda opcional
                elementos.append(Paragraph("Dashboard Financeiro - Análise Concluída", 
                                         estilos["Normal"]))
            else:
                raise FileNotFoundError(f"Arquivo não encontrado: {imagem_path}")
                
        except Exception as e:
            st.warning(f"⚠️ Não foi possível adicionar a imagem final: {e}")
            
            # Adicionar texto alternativo
            elementos.append(Paragraph("✅ Relatório concluído com sucesso!", estilos["Heading3"]))
            elementos.append(Spacer(1, 8))
            elementos.append(Paragraph(f"Período analisado: {titulo_mes}", estilos["Normal"]))
            elementos.append(Paragraph(f"Saldo final: R$ {saldo:,.2f}", estilos["Normal"]))
            elementos.append(Paragraph(f"Total de movimentações: {len(df_pdf)}", estilos["Normal"]))
        
        # Rodapé
        
        pdf.build(elementos)
        buffer.seek(0)
        return buffer

    # -----------------------------
    # Botão para exportar PDF
    # Criar lista de figuras para o PDF
    figuras_para_pdf = [fig_resumo, fig_donut, fig_gastos]
    
    # Gerar PDF com a imagem
    pdf_buffer = gerar_pdf(
        df_mes,
        titulo_mes,
        total_entradas,
        total_saidas,
        saldo,
        figuras_para_pdf,
        caminho_imagem
    )

    st.download_button(
        "📄 Exportar PDF Completo",
        pdf_buffer,
        file_name=f"relatorio_financeiro_{titulo_mes}.pdf",
        mime="application/pdf"
    )
    
    # Mostrar preview da imagem que será usada
    with st.expander("👁️ Visualizar imagem que será incluída no PDF"):
        try:
            if os.path.exists(caminho_imagem):
                st.image(caminho_imagem, caption="Imagem que será adicionada ao final do PDF", 
                        use_container_width=True)
                st.write(f"**Localização do arquivo:** `{caminho_imagem}`")
                st.write(f"**Tamanho:** {os.path.getsize(caminho_imagem) / 1024:.1f} KB")
            else:
                st.error("Arquivo de imagem não encontrado!")
        except Exception as e:
            st.error(f"Erro ao carregar imagem: {e}")

else:
    st.info("Faça upload de um arquivo CSV para visualizar o dashboard.")
    
    # Mostrar instruções sobre a imagem
    with st.expander("ℹ️ Sobre a imagem no PDF"):
        st.write("""
        **Para incluir uma imagem personalizada no PDF:**
        
        1. Coloque um arquivo chamado `image.png` na raiz do seu projeto
        2. A imagem será automaticamente adicionada ao final do relatório PDF
        3. Formato recomendado: PNG, JPG ou JPEG
        4. Dimensões recomendadas: 800x600 pixels ou proporção similar
        
        **Localizações verificadas:**
        - `image.png` (raiz do projeto)
        - `./image.png`
        - Caminho atual do script
        
        Se o arquivo não for encontrado, será criada uma imagem temporária.
        """)
        
        # Exemplo de estrutura do CSV
        st.write("**Exemplo de estrutura do CSV:**")
        exemplo_csv = """data,descricao,categoria,valor,tipo
2024-01-01,Salário,Salário,3000.00,entrada
2024-01-02,Supermercado,Alimentação,-250.50,saida
2024-01-03,Conta de Luz,Utilidades,-150.00,saida
2024-01-04,Freelance,Freelance,500.00,entrada
2024-01-05,Transporte,Transporte,-50.00,saida"""
        
        st.code(exemplo_csv, language="csv")