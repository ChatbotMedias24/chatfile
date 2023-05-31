from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
import streamlit as st
from streamlit_chat import message
from utils import *
from langdetect import detect
from translate import Translator

translator = Translator(to_lang="fr")

# Créer une colonne pour l'image
# Définir le style CSS pour déplacer l'image vers la gauche

st.subheader("Rapport d'activité 2022 de l'Administration des Douanes et Impôts Indirects")

if 'responses' not in st.session_state:
    st.session_state['responses'] = ["Quelle information souhaitez-vous obtenir du rapport annuel sur la situation des droits de l'homme au Maroc 2022 ?"]

if 'requests' not in st.session_state:
    st.session_state['requests'] = []

llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=st.secrets["open_api_key"])

if 'buffer_memory' not in st.session_state:
            st.session_state.buffer_memory=ConversationBufferWindowMemory(k=3,return_messages=True)


system_msg_template = SystemMessagePromptTemplate.from_template(template="""Answer the question as truthfully as possible using the provided context, 
and if the answer is not contained within the text below, say 'I don't know'""")


human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")

prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])

conversation = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template, llm=llm, verbose=True)

# container for chat history
response_container = st.container()
# container for text box
textcontainer = st.container()
query = st.text_input("Posez votre question au chatbot :")
with textcontainer:
    logo_path = "medias24.png"
    logoo_path="rapprt.png"
    st.sidebar.image(logo_path,width=200)
# Définir la structure de colonnes
    left_co, _, right_co = st.sidebar.columns([0.4, 1, 1])

# Déplacer l'image vers la droite
    with right_co:
      st.sidebar.image(logoo_path, width=150,use_column_width="always")
 

    st.sidebar.subheader("Suggestions:")
    st.sidebar.markdown("##### Choisir:")
    questions = [
    "Le résumé du rapport",
    "Quelles sont les mesures tarifaires importantes prises dans le cadre de la Loi de Finances 2022 en matière de fiscalité douanière ?",
    "Quelles sont les mesures prises pour faciliter les opérations sous régimes suspensifs ?",
    "Comment la dématérialisation du bon à délivrer a-t-elle amélioré les procédures douanières ?",
    "Quels sont les résultats de la lutte contre le trafic illicite d'espèces animales protégées menacées d'extinction ?"
]

    selected_questions = []

    for question in questions:
     if st.sidebar.checkbox(question):
        selected_questions.append(question)  
    if selected_questions:
        for selected_question in selected_questions:
          question = selected_question
        if question:
         with st.spinner("En train de taper..."):
            context = find_match(question)
            response = conversation.predict(input=f"Context:\n {context} \n\n Query:\n{question}")
            if detect(response)=='en':
                response = translator.translate(response)
         st.session_state.requests.append(question)
         st.session_state.responses.append(response)
    elif query:
        with st.spinner("En train de taper..."):

            context = find_match(query)
            response = conversation.predict(input=f"Context:\n {context} \n\n Query:\n{query}")
            if detect(response)=='en':
                response = translator.translate(response)
        st.session_state.requests.append(query)
        st.session_state.responses.append(response)
        
 
with response_container:
    if st.session_state['responses']:

        for i in range(len(st.session_state['responses'])):
            message(st.session_state['responses'][i],key=str(i))
            if i < len(st.session_state['requests']):
                message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user')

