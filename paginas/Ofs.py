import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
import plotly.express as px

# Initialize the DataFrame at the start to prevent NameError
df = pd.DataFrame()

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
    .filter-box {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Load data function with improved error handling
@st.cache_data
def load_data(uploaded_file):
    try:
        if uploaded_file is not None:
            # Try with different engines if needed
            try:
                df = pd.read_excel(uploaded_file, engine='openpyxl')
            except:
                df = pd.read_excel(uploaded_file, engine='xlrd')
            
            # Check for required columns and rename if needed
            column_mapping = {
                'FINAL': 'Final',
                'SALDO': 'Saldo',
                'PLANO': 'Plano',
                'ORDEM_F': 'Ordem F',
                'SUB-G': 'Sub-g',
                'INICIO': 'Inicio'
            }
            
            # Rename columns if they exist with different names
            for old_name, new_name in column_mapping.items():
                if old_name in df.columns and new_name not in df.columns:
                    df.rename(columns={old_name: new_name}, inplace=True)
            
            # Convert dates - handle errors
            date_columns = ['Final', 'Inicio']
            for col in date_columns:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], format='%d/%m/%Y', errors='coerce')
                else:
                    st.warning(f"Column '{col}' not found in the Excel file")
            
            # Create Saldo column if it doesn't exist but we have PROGRAMADO and PRODUZIDO
            if 'Saldo' not in df.columns and all(col in df.columns for col in ['PROGRAMADO', 'PRODUZIDO']):
                df['Saldo'] = df['PROGRAMADO'] - df['PRODUZIDO']
            
            # Remove rows with invalid dates
            df = df.dropna(subset=date_columns)
            
            return df
        else:
            return pd.DataFrame()
        
    except Exception as e:
        st.error(f"Failed to load data: {str(e)}")
        return pd.DataFrame()  # Return empty DataFrame on error

def main():
    st.title("🧾 Dashboard de Ordens de Fabricação")
    st.markdown("---")
    
    # Upload file in main content (not sidebar)
    with st.expander("📤 Carregar Dados", expanded=True):
        uploaded_file = st.file_uploader("Selecione o arquivo Excel com os dados das OFs", type=["xlsx", "xls"])
        
        if uploaded_file is not None:
            df = load_data(uploaded_file)
        else:
            st.warning("Por favor, carregue um arquivo Excel para visualizar o dashboard")
            return

    # Data processing
    if not df.empty:
        hoje = pd.to_datetime(date.today())  # Ensure datetime64 type

        # Check if required columns exist before processing
        required_columns = ['Final', 'Saldo', 'Plano']
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            st.error(f"Colunas obrigatórias faltando: {', '.join(missing_columns)}")
            return

        # Process data
        df['Situação'] = np.where(df["Final"] > hoje, 'futura', 'atrasada')
        df['status'] = df['Saldo'].apply(lambda x: 'fechada' if x == 0 else 'aberta')
        df['Tipo_Lote'] = df['Plano'].astype(str).apply(
            lambda x: 'Pedido' if x.startswith('25') and len(x) == 5 else 'Paralelo'
        )

        # Filters in main content
        with st.expander("🔍 Filtros", expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                # Filter by lot type
                tipo_lote = st.multiselect(
                    "Tipo de Lote",
                    options=df['Tipo_Lote'].unique(),
                    default=df['Tipo_Lote'].unique()
                )
            
            with col2:
                # Filter by plan
                planos_disponiveis = df['Plano'].unique()
                plano_selecionado = st.multiselect(
                    "Plano",
                    options=planos_disponiveis,
                    default=[]
                )
            
            with col3:
                # Filter by status
                status_options = df['status'].unique()
                status_selecionado = st.multiselect(
                    "Status",
                    options=status_options,
                    default=status_options
                )
            
            with col4:
                # Filter by situation
                situacao_options = df['Situação'].unique()
                situacao_selecionado = st.multiselect(
                    "Situação",
                    options=situacao_options,
                    default=situacao_options
                )

        # Apply filters
        df_filtrado = df.copy()
        if tipo_lote:
            df_filtrado = df_filtrado[df_filtrado['Tipo_Lote'].isin(tipo_lote)]
        if plano_selecionado:
            df_filtrado = df_filtrado[df_filtrado['Plano'].isin(plano_selecionado)]
        if status_selecionado:
            df_filtrado = df_filtrado[df_filtrado['status'].isin(status_selecionado)]
        if situacao_selecionado:
            df_filtrado = df_filtrado[df_filtrado['Situação'].isin(situacao_selecionado)]

        # KPI cards
        st.markdown('<div class="section-title">Indicadores Principais</div>', unsafe_allow_html=True)
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">OFs Totais</div>
                <div class="kpi-value">{len(df_filtrado):,}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">OFs Abertas</div>
                <div class="kpi-value">{(df_filtrado['status'] == 'aberta').sum():,}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            ofs_atrasadas_abertas = df_filtrado[
                (df_filtrado['Situação'] == 'atrasada') & (df_filtrado['status'] == 'aberta')
            ].shape[0]
            
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">OFs Atrasadas</div>
                <div class="kpi-value negative">{ofs_atrasadas_abertas:,}</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">OFs Fechadas</div>
                <div class="kpi-value positive">{(df_filtrado['status'] == 'fechada').sum():,}</div>
            </div>
            """, unsafe_allow_html=True)

        with col5:
            ofs_fechadas_hoje = df_filtrado[
                (df_filtrado['status'] == 'fechada') & 
                (df_filtrado['Final'].dt.date == date.today())
            ].shape[0]
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">OFs Fechadas Hoje</div>
                <div class="kpi-value positive">{ofs_fechadas_hoje:,}</div>
            </div>
            """, unsafe_allow_html=True)

        # Time evolution chart
        st.markdown('<div class="section-title">Evolução de OFs Fechadas</div>', unsafe_allow_html=True)

        # Time period filter
        col6, col7, col8 = st.columns(3)
        with col6:
            periodo = st.selectbox("Período", ["Semanal", "Mensal", "Anual"], index=1)

        # Prepare data for the chart
        df_fechadas = df_filtrado[df_filtrado['status'] == 'fechada'].copy()
        df_fechadas = df_fechadas.dropna(subset=['Final'])
        df_fechadas['Final'] = pd.to_datetime(df_fechadas['Final'], errors='coerce')

        # Define o intervalo de datas
        data_fim = date.today()
        if periodo == "Semanal":
            data_inicio = data_fim - timedelta(days=7)
        elif periodo == "Mensal":
            data_inicio = data_fim - timedelta(days=30)
        else:  # Anual
            data_inicio = data_fim - timedelta(days=365)

        # Gera a série de datas
        datas_completas = pd.date_range(start=data_inicio, end=data_fim).date

        # Agrupa as OFs fechadas por data
        df_fechadas['Periodo'] = df_fechadas['Final'].dt.date
        contagem_temporal = df_fechadas.groupby('Periodo').size()

        # Reindexa para incluir todas as datas no range
        contagem_temporal = contagem_temporal.reindex(datas_completas, fill_value=0).reset_index()
        contagem_temporal.columns = ['Periodo', 'Quantidade']

        # Plotly chart
        fig = px.line(contagem_temporal, x='Periodo', y='Quantidade',
                    title=f"Evolução de OFs Fechadas - {periodo}",
                    markers=True, line_shape='spline')
        fig.update_traces(line=dict(width=3))
        fig.update_layout(hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)

        # Últimas OFs Entregues
        st.markdown('<div class="section-title">Últimas OFs Entregues</div>', unsafe_allow_html=True)

        # Filtro para fechadas, ordena pela data final decrescente
        ultimas_entregues = df_filtrado[df_filtrado['status'] == 'fechada'].sort_values('Final', ascending=False).head(10)

        # Exibe a tabela
        st.dataframe(
            ultimas_entregues[['Ordem F', 'Plano', 'Sub-g', 'status', 'Final']],
            use_container_width=True
        )

        # Plan analysis section
        st.markdown('<div class="section-title">Análise por Plano</div>', unsafe_allow_html=True)

        # Filter only 25XXX plans for specific analysis
        df_25xxx = df_filtrado[df_filtrado['Plano'].astype(str).str.match(r'^25\d{3}$')]
        if not df_25xxx.empty:
            contagem_por_plano = df_25xxx.groupby(['Plano', 'status']).size().unstack(fill_value=0)
            total_por_plano = contagem_por_plano.sum(axis=1)
            contagem_porcentagem = (contagem_por_plano.div(total_por_plano, axis=0)) * 100

            col9, col10 = st.columns(2)
            with col9:
                st.write("**Quantidade por Plano (25XXX)**")
                st.dataframe(contagem_por_plano.style.background_gradient(cmap='Blues'), 
                            use_container_width=True)

            with col10:
                st.write("**Porcentagem por Plano (25XXX)**")
                st.dataframe(contagem_porcentagem.style.format("{:.1f}%").background_gradient(cmap='Greens'), 
                            use_container_width=True)
        else:
            st.warning("Nenhum plano 25XXX encontrado para análise.")

        # Pie charts section
        st.markdown('<div class="section-title">Distribuição de OFs</div>', unsafe_allow_html=True)

        # Create two columns
        col1, col2 = st.columns(2)

        with col1:
            # Count the occurrences of each Tipo_Lote
            tipo_lote_count = df_filtrado['Tipo_Lote'].value_counts()

            # Plotting the pie chart for Tipo_Lote
            fig_tipo_lote = px.pie(tipo_lote_count, values=tipo_lote_count.values, names=tipo_lote_count.index, 
                                title="Distribuição por Tipo de Lote", 
                                color=tipo_lote_count.index, 
                                color_discrete_map={'Pedido': 'lightblue', 'Paralelo': 'lightgreen'})
            fig_tipo_lote.update_traces(textinfo='percent+label', pull=[0.1, 0.1])
            st.plotly_chart(fig_tipo_lote, use_container_width=True)

        with col2:
            # Mapping sub-g values to the specific categories
            df_filtrado['Sub-g'] = df_filtrado['Sub-g'].replace({1: 'Montagem', 2: 'Solda', 3: 'Estamparia'})

            # Count the occurrences of each Sub-g category
            sub_g_count = df_filtrado['Sub-g'].value_counts()

            # Plotting the pie chart for Sub-g
            fig_sub_g = px.pie(sub_g_count, values=sub_g_count.values, names=sub_g_count.index, 
                            title="Distribuição por Sub-grupo", 
                            color=sub_g_count.index, 
                            color_discrete_map={'Montagem': 'lightcoral', 'Solda': 'lightblue', 'Estamparia': 'lightgreen'})
            fig_sub_g.update_traces(textinfo='percent+label', pull=[0.1, 0.1, 0.1])
            st.plotly_chart(fig_sub_g, use_container_width=True)
    else:
        st.warning("Nenhum dado válido encontrado no arquivo carregado.")

if __name__ == "__main__":
    main()
