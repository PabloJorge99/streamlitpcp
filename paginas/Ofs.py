import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import os

def main():
    st.title("📄 Ordens de Fabricação (OFs)")
    st.markdown("Visualização geral das ordens de fabricação.")

    # === Carregar dados ===
    try:
        df = pd.read_csv(os.path.join("data", "ofs.csv"), parse_dates=["FINAL", "INICIO", "ENTREGA"])
    except FileNotFoundError:
        st.error("Arquivo `ofs.csv` não encontrado.")
        return

    # === Preprocessamento ===
    hoje = pd.Timestamp.today().normalize()
    ontem = hoje - pd.Timedelta(days=1)

    # Considerar "fechadas" as que têm FINAL preenchido
    fechadas = df[df["FINAL"].notna()]
    abertas = df[df["FINAL"].isna()]
    atrasadas = abertas[abertas["ENTREGA"] < hoje]

    # Fechadas ontem
    fechadas_ontem = fechadas[fechadas["FINAL"] == ontem]

    # Fechadas anteontem (para % evolução)
    anteontem = hoje - pd.Timedelta(days=2)
    fechadas_anteontem = fechadas[fechadas["FINAL"] == anteontem]

    # === KPIs ===
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🔓 OFs Abertas", len(abertas))
    col2.metric("⚠️ Atrasadas", len(atrasadas))
    col3.metric("✅ Fechadas", len(fechadas))
    
    evolucao = len(fechadas_ontem) - len(fechadas_anteontem)
    perc = (evolucao / len(fechadas_anteontem) * 100) if len(fechadas_anteontem) > 0 else 0
    col4.metric("📆 Fechadas ontem", len(fechadas_ontem), f"{perc:.1f}%")

    st.markdown("---")

    # === Gráfico de linha: OFs fechadas por dia útil ===
    fechadas["DATA"] = fechadas["FINAL"].dt.date
    fechamento_dia = fechadas.groupby("DATA").size().reset_index(name="Quantidade")
    fechamento_dia = fechamento_dia[~pd.to_datetime(fechamento_dia["DATA"]).dt.dayofweek.isin([5, 6])]  # dias úteis

    fig1 = px.line(fechamento_dia, x="DATA", y="Quantidade", markers=True, title="📈 OFs Fechadas por Dia Útil")
    st.plotly_chart(fig1, use_container_width=True)

    # === Gráfico de pizza: distribuição por setor (SUB-G) ===
    setor_map = {1: "Montagem", 2: "Solda", 3: "Estamparia/Usinagem"}
    abertas["Setor"] = abertas["SUB-G"].map(setor_map)
    setor_counts = abertas["Setor"].value_counts().reset_index()
    setor_counts.columns = ["Setor", "Total"]

    fig2 = px.pie(setor_counts, names="Setor", values="Total", title="🧩 Abertas por Setor")
    st.plotly_chart(fig2, use_container_width=True)

    # === Gráfico de pizza: abertas vs atrasadas ===
    situacao = pd.Series({
        "Abertas no Prazo": len(abertas) - len(atrasadas),
        "Abertas Atrasadas": len(atrasadas)
    }).reset_index()
    situacao.columns = ["Status", "Quantidade"]

    fig3 = px.pie(situacao, names="Status", values="Quantidade", title="⏱️ Situação das OFs Abertas")
    st.plotly_chart(fig3, use_container_width=True)

    # === Últimas 5 OFs fechadas por setor ===
    fechadas["Setor"] = fechadas["SUB-G"].map(setor_map)
    st.markdown("### 🧾 Últimas 5 OFs Fechadas por Setor")
    for setor in setor_map.values():
        ultimas = fechadas[fechadas["Setor"] == setor].sort_values("FINAL", ascending=False).head(5)
        if not ultimas.empty:
            st.markdown(f"**{setor}**")
            st.dataframe(ultimas[["ORDEM_F", "PRODUTO", "DESCRIÇÃO", "FINAL", "PLANO"]], use_container_width=True)

if __name__ == "__main__":
    main()
