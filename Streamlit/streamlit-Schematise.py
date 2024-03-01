import streamlit as st
import pandas as pd
import numpy as np
import model, metamodelAndRAG, seconddraftCombinedProcess, utils

@st.cache_data
def load_data(filename, start_value, end_value):

    df2 = utils.csv_parser(filename, int(start_value), int(end_value))
    return df2

st.write(
        "Upload a csv file in the same format as 'fullsections.csv' available at https://raw.githubusercontent.com/sankalpsrv/Schematise/dev/fullsections.csv")
filename = "fullsections.csv"
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    filename = uploaded_file.name

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
        options=["None", "openaiselected", "Llama2-7b-chat-GPTQ"],
    )
df2 = load_data(filename, start_value, end_value)

XML_responses = seconddraftCombinedProcess.responseGetter(df2, llm_selected, format_chosen)

st.write(XML_responses)







