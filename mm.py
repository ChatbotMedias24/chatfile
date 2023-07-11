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

st.subheader("Rapport Marocains du Monde")

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
    left_co, _, right_co = st.sidebar.columns([0.4, 1, 1])

    # Ajouter un espace vide à gauche pour déplacer l'image vers la droite
    spacer = left_co.empty()

    # Afficher l'image
    #with right_co:
        #st.sidebar.image(logoo_path, width=200)

    st.sidebar.subheader("Suggestions:")
    st.sidebar.markdown("##### Choisir:")
    questions = [
        "Le résumé du rapport",
        "Quelles sont les conditions d'octroi des franchises et tolérances pour les effets personnels ?",
        "Comment obtenir l'admission temporaire pour mon véhicule lors de mon séjour au Maroc ?",
        "Quelles sont les formalités à remplir pour importer des pièces de rechange pour mon véhicule ?",
        "Quels sont les services douaniers disponibles pour les voyageurs au Maroc ?"
    ]

    selected_questions = []

    for question in questions:
        if st.sidebar.checkbox(question):
            selected_questions.append(question)  
    if selected_questions:
        for selected_question in selected_questions:
            if selected_question == "Le résumé du rapport":
                response = "Le résumé du rapport est de fournir des informations sur les différents régimes douaniers applicables au Maroc, tels que l'admission temporaire et la détaxe aux frontières. Le rapport explique les conditions et les procédures pour bénéficier de ces régimes, notamment en ce qui concerne l'importation de pièces de rechange, la conduite d'un véhicule en admission temporaire par une tierce personne résidente à l'étranger, et le remboursement de la taxe sur la valeur ajoutée (TVA) pour les achats non commerciaux destinés à être utilisés à l'étranger. Le rapport précise également que les bénéficiaires de l'admission temporaire sont responsables de la réexportation du véhicule ou de son dédouanement selon les réglementations en vigueur, et qu'en cas de décès du bénéficiaire, des dispositions sont prévues pour le rapatriement du véhicule par les ayants droit."
                st.session_state.requests.append(selected_question)
                st.session_state.responses.append(response)
            elif selected_question == "Quelles sont les conditions d'octroi des franchises et tolérances pour les effets personnels ?":
                response = "Les conditions d'octroi des franchises et tolérances pour les effets personnels sont les suivantes :- Un séjour effectif à l'étranger d'au moins 10 ans, ou en retour définitif au pays.- Les bijoux personnels, votre instrument de musique portatif, votre ordinateur portable, un fauteuil roulant à propulsion manuelle ou électrique et autres accessoires orthopédiques à usage strictement personnel, vos équipements de sport légers sont autorisés en franchise.- Les vélomoteurs et les bicyclettes (sauf celles pour enfants), les meubles, les tapis (la franchise n'est autorisée que pour un seul tapis), les appareils électroménagers à l'état neuf ou d'occasion, les appareils de télévision et autres appareils similaires ne sont pas autorisés en franchise et sont soumis à des formalités douanières spécifiques."
                st.session_state.requests.append(selected_question)
                st.session_state.responses.append(response)
            elif selected_question == "Quels sont les services douaniers disponibles pour les voyageurs au Maroc ?":
                response = "Au Maroc, les services douaniers sont disponibles dans les gares maritimes, les aéroports et les frontières terrestres. Ils sont à la disposition des voyageurs tout au long de l'année. Pendant la période estivale, il existe également l'opération Marhaba où les services douaniers renforcent leur présence pour faciliter le passage des voyageurs. De plus, en cas de décès du bénéficiaire du régime de l'AT (Admission Temporaire), les services douaniers autorisent les ayants droit ou toute personne mandatée par eux à rapatrier le véhicule à l'étranger ou à le dédouaner selon les conditions réglementaires."
                st.session_state.requests.append(selected_question)
                st.session_state.responses.append(response)
            elif selected_question == "Comment obtenir l'admission temporaire pour mon véhicule lors de mon séjour au Maroc ?":
                response = "Pour obtenir l'admission temporaire pour votre véhicule lors de votre séjour au Maroc, vous devez suivre les étapes suivantes :1. Présentez-vous aux services douaniers avec les documents requis, tels que le titre de séjour pour les étrangers résidant au Maroc, la carte d'admission temporaire, et la facture d'achat originale pour les voitures de moins de trois mois.2. Souscrivez un engagement sur l'honneur affirmant que vous régulariserez la situation douanière de votre véhicule dès votre retour au Maroc et que le véhicule ne sera pas utilisé par une tierce personne.3. Assurez-vous de respecter le délai d'admission temporaire pour éviter tout contentieux relatif au dépassement du délai.Veuillez noter que ces informations sont basées sur le contexte fourni, mais il est toujours recommandé de vérifier les exigences spécifiques auprès des services douaniers marocains pour obtenir les informations les plus à jour.."
                st.session_state.requests.append(selected_question)
                st.session_state.responses.append(response)
            elif selected_question == "Quelles sont les formalités à remplir pour importer des pièces de rechange pour mon véhicule ?":
                response = "Pour importer des pièces de rechange pour votre véhicule au Maroc, vous devez remplir les formalités suivantes :1. Les pièces de rechange importées doivent être enregistrées sur le système informatique de l'Administration des Douanes et Impôts Indirects au nom de l'importateur du véhicule.2. Les pièces remplacées doivent être réexportées à la fin du séjour du véhicule au Maroc, ou éventuellement, être dédouanées en payant les droits et taxes exigibles.Veuillez noter que ces informations sont basées sur le contexte fourni, mais il est toujours recommandé de vérifier les exigences spécifiques auprès des services douaniers marocains pour obtenir les informations les plus à jour."
                st.session_state.requests.append(selected_question)
                st.session_state.responses.append(response)
            
            else:
                question = selected_question
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
