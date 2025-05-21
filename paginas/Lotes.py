import streamlit as st
import plotly.graph_objects as go
import streamlit.components.v1 as components

def main():
    st.title("Lotes")
    st.markdown("---")

lotes = [
    {"id": "25210", "progresso": 11},
    {"id": "25209", "progresso": 12},
    {"id": "25208", "progresso": 23},
    {"id": "25207", "progresso": 27},
    {"id": "25206", "progresso": 38},
    {"id": "25205", "progresso": 41},
    {"id": "25204", "progresso": 48},
    {"id": "25203", "progresso": 59},
    {"id": "25202", "progresso": 65},
    {"id": "25201", "progresso": 74},
    {"id": "25200", "progresso": 82},
    {"id": "25199", "progresso": 88},
]

def gerar_gradiente(index, total):
    if index < total / 3:
        return "linear-gradient(135deg, #00cc66, #ccff66)"  # verde
    elif index < 2 * total / 3:
        return "linear-gradient(135deg, #ffcc00, #ff9966)"  # amarelo
    else:
        return "linear-gradient(135deg, #ff6666, #cc0000)"  # vermelho

def gauge_plot(valor):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=valor,
        number={'suffix': "%", 'font': {'size': 22, 'color': "white"}},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100], 'visible': False},
            'bar': {'color': "#FFD700", 'thickness': 0.7},
            'bgcolor': "lightgray",
            'shape': "angular",
        }
    ))
    fig.update_layout(
        margin=dict(t=10, b=0, l=0, r=0),
        height=180,
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig.to_html(include_plotlyjs="cdn", full_html=False)

cols = st.columns(4)

for i, lote in enumerate(lotes):
    gradient = gerar_gradiente(i, len(lotes))
    with cols[i % 4]:
        html = f"""
        <div style='
            background: {gradient};
            padding: 15px;
            border-radius: 20px;
            margin-bottom: 10px;
            text-align: center;
            color: white;
        '>
            <div style='font-size: 16px; font-weight: bold; margin-bottom: 10px;'>Lote {lote["id"]}</div>
            {gauge_plot(lote["progresso"])}
        </div>
        """
        components.html(html, height=250)

if __name__ == "__main__":
    main()
