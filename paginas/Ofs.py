import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

# Custom CSS for KPIs
st.markdown("""
<style>
    .kpi-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin-bottom: 20px;
    }
    .kpi-title {
        font-size: 16px;
        color: #4a4a4a;
        margin-bottom: 10px;
        font-weight: 600;
    }
    .kpi-value {
        font-size: 28px;
        font-weight: 700;
        color: #2c3e50;
    }
    .positive {
        color: #27ae60;
    }
    .negative {
        color: #e74c3c;
    }
    .section-title {
        font-size: 20px;
        color: #2c3e50;
        margin-top: 30px;
        margin-bottom: 15px;
        font-weight: 700;
        border-bottom: 2px solid #3498db;
        padding-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Page configuration
    st.set_page_config(layout="wide", page_title="Dashboard de OFs")
    
    st.title("📄 Dashboard de Ordens de Fabricação (OFs)")
    
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
    
    # Add status columns
    df['status'] = df['SALDO'].apply(lambda x: 'fechada' if x == 0 else 'aberta')
    df['Situação'] = np.where(df["FINAL"] > hoje, 'futura', 'atrasada')
    
    fechadas = df[df["FINAL"].notna()]
    abertas = df[df["FINAL"].isna()]
    atrasadas = abertas[abertas["ENTREGA"] < hoje]
    fechadas_ontem = fechadas[fechadas["FINAL"].dt.date == ontem.date()]
    fechadas_anteontem = fechadas[fechadas["FINAL"].dt.date == anteontem.date()]

    # Sidebar filters
    with st.sidebar:
        st.title("Filtros")
        
        # Filter by status
        status_options = df['status'].unique()
        status_selecionado = st.multiselect(
            "Status",
            options=status_options,
            default=status_options
        )
        
        # Filter by situation
        situacao_options = df['Situação'].unique()
        situacao_selecionado = st.multiselect(
            "Situação",
            options=situacao_options,
            default=situacao_options
        )
        
        # Filter by SUB-G
        sub_g_options = df['SUB-G'].unique()
        sub_g_selecionado = st.multiselect(
            "Sub-Grupo",
            options=sub_g_options,
            default=sub_g_options
        )

    # Apply filters
    df_filtrado = df.copy()
    if status_selecionado:
        df_filtrado = df_filtrado[df_filtrado['status'].isin(status_selecionado)]
    if situacao_selecionado:
        df_filtrado = df_filtrado[df_filtrado['Situação'].isin(situacao_selecionado)]
    if sub_g_selecionado:
        df_filtrado = df_filtrado[df_filtrado['SUB-G'].isin(sub_g_selecionado)]

    # Update filtered data
    fechadas = df_filtrado[df_filtrado["FINAL"].notna()]
    abertas = df_filtrado[df_filtrado["FINAL"].isna()]
    atrasadas = abertas[abertas["ENTREGA"] < hoje]
    fechadas_ontem = fechadas[fechadas["FINAL"].dt.date == ontem.date()]
    fechadas_anteontem = fechadas[fechadas["FINAL"].dt.date == anteontem.date()]

    # === KPIs ===
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">OFs Abertas</div>
            <div class="kpi-value">{len(abertas):,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">OFs Atrasadas</div>
            <div class="kpi-value negative">{len(atrasadas):,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">OFs Fechadas</div>
            <div class="kpi-value positive">{len(fechadas):,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        evolucao = len(fechadas_ontem) - len(fechadas_anteontem)
        perc = (evolucao / len(fechadas_ante
