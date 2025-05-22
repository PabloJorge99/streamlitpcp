import streamlit as st

def main():
    st.title("Programação")
    st.markdown("---")
    
    # Inicializar dados na session state se não existirem
    if 'dados' not in st.session_state:
        st.session_state.dados = [
            {"Lote": "24328", "Descrição": "PLANTADEIRAS AGCO", "Cor": "pink", "Programar": True, "Cálculo NEC": False, "Gerar SOC": False, "E-mail SOC": False, "Gerar OF": True},
            {"Lote": "24431", "Descrição": "PLAINAS C", "Cor": "magenta", "Programar": True, "Cálculo NEC": True, "Gerar SOC": True, "E-mail SOC": True, "Gerar OF": True},
        ]
    
    # Formulário para adicionar nova OF
    with st.expander("➕ Adicionar novo Lote"):
        with st.form("nova_of"):
            lote = st.text_input("Lote")
            descricao = st.text_input("Descrição")
            cor = st.color_picker("Cor do Lote", "#FF69B4")
            
            programar = st.checkbox("Programar", value=True)
            calc_nec = st.checkbox("Cálculo NEC", value=False)
            gerar_soc = st.checkbox("Gerar SOC", value=False)
            email_soc = st.checkbox("E-mail SOC", value=False)
            gerar_of = st.checkbox("Gerar OF", value=True)

            submitted = st.form_submit_button("Adicionar")
            if submitted:
                novo_item = {
                    "Lote": lote,
                    "Descrição": descricao,
                    "Cor": cor,
                    "Programar": programar,
                    "Cálculo NEC": calc_nec,
                    "Gerar SOC": gerar_soc,
                    "E-mail SOC": email_soc,
                    "Gerar OF": gerar_of
                }
                st.session_state.dados.append(novo_item)
                st.success(f"Nova OF '{lote}' adicionada!")
                st.rerun()
    
    # Cabeçalho da tabela
    cabecario = st.columns([0.8, 2, 1, 1, 1, 1, 1, 1])

    with cabecario[0]: st.markdown("**Lote**")
    with cabecario[1]: st.markdown("**Descrição**")
    with cabecario[2]: st.markdown("**Cor**")
    with cabecario[3]: st.markdown("**Programar**")
    with cabecario[4]: st.markdown("**Cálculo NEC**")
    with cabecario[5]: st.markdown("**Gerar SOC**")
    with cabecario[6]: st.markdown("**E-mail SOC**")
    with cabecario[7]: st.markdown("**Gerar OF**")
    
    # Renderizar tabela com checkboxes editáveis
    for i, item in enumerate(st.session_state.dados):
        cols = st.columns([0.8, 2, 1, 1, 1, 1, 1, 1])

        with cols[0]: st.markdown(f"**{item['Lote']}**")
        with cols[1]: st.markdown(item['Descrição'])
        with cols[2]: st.markdown(f"<div style='width:25px;height:25px;background-color:{item['Cor']};border-radius:4px'></div>", unsafe_allow_html=True)

        with cols[3]:
            st.session_state.dados[i]['Programar'] = st.checkbox("", value=item['Programar'], key=f"prog_{i}")
        with cols[4]:
            st.session_state.dados[i]['Cálculo NEC'] = st.checkbox("", value=item['Cálculo NEC'], key=f"nec_{i}")
        with cols[5]:
            st.session_state.dados[i]['Gerar SOC'] = st.checkbox("", value=item['Gerar SOC'], key=f"soc_{i}")
        with cols[6]:
            st.session_state.dados[i]['E-mail SOC'] = st.checkbox("", value=item['E-mail SOC'], key=f"email_{i}")
        with cols[7]:
            st.session_state.dados[i]['Gerar OF'] = st.checkbox("", value=item['Gerar OF'], key=f"of_{i}")

if __name__ == "__main__":
    main()
