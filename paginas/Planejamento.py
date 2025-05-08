import streamlit as st

def main():
    st.title("Programação")
    st.markdown("---")
    
# Inicializar dados na session state se não existirem

    if 'dados' not in st.session_state:

        st.session_state.dados = [

            {"Lote": "24328", "Descrição": "PLANTADEIRAS AGCO", "Cor": "pink", "Programar": True, "Estamparia": False, "Aleques": False, "Solda": False, "Usinagem": True},

            {"Lote": "24431", "Descrição": "PLAINAS C", "Cor": "magenta", "Programar": True, "Estamparia": True, "Aleques": True, "Solda": True, "Usinagem": True},

        ]

    

    # Formulário para adicionar nova OF

    with st.expander("➕ Adicionar novo Lote"):

        with st.form("nova_of"):

            lote = st.text_input("Lote")

            descricao = st.text_input("Descrição")

            cor = st.color_picker("Cor do Lote", "#FF69B4")

        

            # Checkboxes para cada etapa

            programar = st.checkbox("Programar", value=True)

            estamparia = st.checkbox("Estamparia", value=False)

            aleques = st.checkbox("Aleques", value=False)

            solda = st.checkbox("Solda", value=False)

            usinagem = st.checkbox("Usinagem", value=True)

        

            submitted = st.form_submit_button("Adicionar")

            if submitted:

                novo_item = {

                    "Lote": lote,

                    "Descrição": descricao,

                    "Cor": cor,

                    "Programar": programar,
                    
                    "Estamparia": estamparia,

                    "Aleques": aleques,

                    "Solda": solda,

                    "Usinagem": usinagem

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

    with cabecario[4]: st.markdown("**Estamparia**")

    with cabecario[5]: st.markdown("**Aleques**")

    with cabecario[6]: st.markdown("**Solda**")

    with cabecario[7]: st.markdown("**Usinagem**")

    

    # Renderizar tabela com checkboxes editáveis

    for i, item in enumerate(st.session_state.dados):

        cols = st.columns([0.8, 2, 1, 1, 1, 1, 1, 1])

    

        with cols[0]: st.markdown(f"**{item['Lote']}**")

        with cols[1]: st.markdown(item['Descrição'])

        with cols[2]: st.markdown(f"<div style='width:25px;height:25px;background-color:{item['Cor']};border-radius:4px'></div>", unsafe_allow_html=True)

    

        # Checkboxes para cada etapa

        with cols[3]:

            if st.checkbox("", value=item['Programar'], key=f"prog_{i}"):

                st.session_state.dados[i]['Programar'] = True

            else:

                st.session_state.dados[i]['Programar'] = False

    

        with cols[4]:

            if st.checkbox("", value=item['Estamparia'], key=f"est_{i}"):

                st.session_state.dados[i]['Estamparia'] = True

            else:

                st.session_state.dados[i]['Estamparia'] = False

    

        with cols[5]:

            if st.checkbox("", value=item['Aleques'], key=f"ale_{i}"):

                st.session_state.dados[i]['Aleques'] = True

            else:

                st.session_state.dados[i]['Aleques'] = False

    

        with cols[6]:

            if st.checkbox("", value=item['Solda'], key=f"solda_{i}"):

                st.session_state.dados[i]['Solda'] = True

            else:

                st.session_state.dados[i]['Solda'] = False

    

        with cols[7]:

            if st.checkbox("", value=item['Usinagem'], key=f"usin_{i}"):

                st.session_state.dados[i]['Usinagem'] = True

            else:

                st.session_state.dados[i]['Usinagem'] = False
        
if __name__ == "__main__":
    main()