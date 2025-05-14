import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

def main():
    st.title("📄 Ordens de Fabricação (OFs)")
    st.markdown("Visualização geral das ordens de fabricação.")

    # === Dados fictícios ===
    dados = {
        "ORDEM_F": [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008],
        "PRODUTO": ["Produto A", "Produto B", "Produto C", "Produto D", "Produto E", "Produto F", "Produto G", "Produto H"],
        "DESCRIÇÃO": ["Desc A", "Desc B", "Desc C", "Desc D", "Desc E", "Desc F", "Desc G", "Desc H"],
        "SUB-G": [3, 2, 1, 3, 2, 1, 3, 1],
        "PROGRAMADO": [100, 200, 150, 120, 180, 130, 160, 110],
        "PRODUZIDO": [100, 180, 130, 100, 180, 130, 160, 110],
        "SALDO": [0, 20, 20, 20, 0, 0, 0, 0],
        "INICIO": pd.to_datetime(["2025-05-01", "2025-05-02", "2025-05-02", "2025-05-05", "2025-05-06", "2025-05-06", "2025-05-07", "2025-05-07"]),
        "FINAL": pd.to_datetime(["2025-05-13", "2025-05-14", "2025-05-14", None, None, "2025-05-13", "2025-05-14", None]),
        "PLANO": ["P001", "P002", "P003", "P004", "P005", "P006", "P007", "P008"],
        "LOCAL": ["Fábrica 1", "Fábrica 2", "Fábrica 3", "Fábrica 1", "Fábrica 2", "Fábrica 3", "Fábrica 1", "Fábrica 3"],
        "ENTREGA": pd.to_datetime(["2025-05-14"] * 8),
        "ATRASO": [0] * 8,
        "MATERIA_PRIMA": ["Aço", "Alumínio", "Aço", "Inox", "Latão", "Cobre", "Alumínio", "Cobre"]
    }
    df = pd.DataFrame(dados)

    # === Preprocessamento ===
    hoje = pd.Timestamp.today().normalize()
    ontem = hoje - pd.Timedelta(days=1)
    anteontem = hoje - pd.Timedelta(days=2)

    fechadas = df[df["FINAL"].notna()]
    abertas = df[df["FINAL"].isna()]
    atrasadas = abertas[abertas["ENTREGA"] < hoje]
    fechadas_ontem = fechadas[fechadas["FINAL"].dt.date == ontem.date()]
    fechadas_anteontem = fechadas[fechadas["FINAL"].dt.date == anteontem.date()]

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
    fechamento_dia = fechamento_dia[pd.to_datetime(fechamento_dia["DATA"]).dt.dayofweek < 5]

    fig1 = px.line(fechamento_dia, x="DATA", y="Quantidade", markers=True, title="📈 OFs Fechadas por Dia Útil")
    st.plotly_chart(fig1, use_container_width=True)

    # === Pizza por setor ===
    setor_map = {1: "Montagem", 2: "Solda", 3: "Estamparia/Usinagem"}
    abertas["Setor"] = abertas["SUB-G"].map(setor_map)
    setor_counts = abertas["Setor"].value_counts().reset_index()
    setor_counts.columns = ["Setor", "Total"]

    fig2 = px.pie(setor_counts, names="Setor", values="Total", title="🧩 Abertas por Setor")
    st.plotly_chart(fig2, use_container_width=True)

    # === Pizza abertas vs atrasadas ===
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
