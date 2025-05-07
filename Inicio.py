import streamlit as st

def main():
    st.title("🏠 Página Inicial")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Bem-vindo ao Controle PCP")
        st.markdown("""
        Este sistema permite gerenciar toda a produção da fábrica,
        desde pedidos até os setores operacionais.
        """)
    
    with col2:
        st.subheader("Estatísticas Rápidas")
        st.metric("Pedidos Hoje", 15)
        st.metric("Produção Diária", "85%", "3%")
    

if __name__ == "__main__":
    main()