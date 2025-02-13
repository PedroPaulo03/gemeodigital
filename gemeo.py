import streamlit as st


st.set_page_config(
    page_title="Gemeo Digital",
    page_icon='😒',
    layout="centered",
    initial_sidebar_state="expanded")

st.logo("arquivos/logo.png") 

paginas = {
    "Conteúdos": [
        st.Page("paginas/inicial.py", title="Página Inicial", icon = '', default = True),  
    ], 

    "Aplicativos para os Alunos": [
        st.Page("paginas/chatbot.py", title="DanBot", icon='😁'), 
    ],
}

pg = st.navigation(paginas)
pg.run()
  