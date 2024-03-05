import streamlit as st
import pandas as pd
import numpy as np
import model, metamodelAndRAG, seconddraftCombinedProcess, utils
from decouple import config
ik_api = config('IK_API_KEY', default = '')
openai_key = config('OPENAI_API_KEY', default = '')

@st.cache_data
def set_env(request, key):
    global ik_api, openai_key
    if request == "openai":
        openai_key = key
    else:
        ik_api = key
    with open('.env', 'w') as fn:
        fn.write(f"OPENAI_API_KEY={openai_key}\nIK_API_KEY={ik_api}")
@st.cache_data
def load_data(filename, start_value, end_value):

    df2 = utils.csv_parser(filename, int(start_value), int(end_value))
    return df2

@st.cache_data
def get_XML(df2, llm_selected, format_chosen):
    XML_responses = seconddraftCombinedProcess.responseGetter(df2, llm_selected, format_chosen)
    return XML_responses

condition_for_csv = st.radio("Do you want to upload a CSV file or use your IndianKanoon API key?", ["Upload", "IndianKanoon"])

if condition_for_csv == "Upload":
    st.write(
            "Upload a csv file in the same format as 'fullsections.csv' available at https://raw.githubusercontent.com/sankalpsrv/Schematise/dev/fullsections.csv and shown below")
    filename = "fullsections.csv"

    dftest = pd.read_csv("fullsections.csv")

    dftest2 = dftest.head(5)

    st.table(dftest2)

    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        filename = uploaded_file.name

else:
    ik_api=st.text_input("Please enter your IndianKanoon API Key")
    set_env()
    if ik_api is not '':
        docnumber=st.text_input("Specify a document number to get from IndianKanoon")



format_chosen=st.radio(
        "Choose LegalDocML/AkomaNtoso or LegalRuleML 👉",
        key="format_chosen",
        options=["None", "legaldocml", "legalruleml"],
    )


start_value = st.text_input('Starting range', '71')
end_value = st.text_input('Ending range', '73')
llm_selected = st.radio(
        "Choose OpenAI or Llama2 👉",
        key="llm_selected",
        options=["None", "OpenAI", "Llama2-7b-chat-GPTQ"],
    )
df2 = load_data(filename, start_value, end_value)

if llm_selected == 'OpenAI':
    openai_key = st.text_input("OpenAI API Key")
    set_env("openai", openai_key)
    
XML_responses = get_XML(df2, llm_selected, format_chosen)

st.write(XML_responses)

st.session_state['XML_resp'] = XML_responses

st.session_state['fchosen'] = format_chosen

st.session_state['llmc'] = llm_selected










