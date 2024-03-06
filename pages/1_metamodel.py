
import streamlit as st
import pandas as pd
import numpy as np
import model, metamodelAndRAG, combinedProcess, utils
#from Schematise import XML_responses, format_chosen


XML_responses = st.session_state['XML_resp']
format_chosen = st.session_state['fchosen']
llm_selected = st.session_state['llmc']
openai_key = st.session_state['openai_key']
ik_api = st.session_state['ik_api']

def metamodel_options(key_id):

    key_id_2 = "metamodel" + str(key_id)
    key_id_3 = "numbers" + str(key_id)
    key_id_4 = "metamodel_sel" + str(key_id)
    key_id_5 = "error" + str(key_id)
    metamodels_to_process = []
    st.write(
        "The following metamodels can be used to align the new XML generation: (Input anything other than integers 1-7 to continue", key=key_id_2)

    option = st.selectbox(
    'Which metamodel would you like to align your LegalRuleML output with?', ('1. Context', '2. Defeasible', '3. Deontic', '4. Legal Temporal', '5. Metadata-actor', '6. Metadata jurisdiction authority', '7. Statement'), key=key_id_3)


    metamodel_selected = str(int(option.split('.')[0]))
    # Break the loop if the input is not an integer between 1 and 7 or if it's an empty string
    if not metamodel_selected.isdigit() or int(metamodel_selected) not in range(1, 8):
        st.write("Invalid input. Please enter a number between 1 and 7, or press enter to finish.", key=key_id_5)
        # Prompt the user again for a valid input

    # If the input is valid, add it to the list of metamodels to process
    metamodels_to_process.append(metamodel_selected)

    return metamodels_to_process

@st.cache_data
def cache_XML_responses(XML_responses):
    new_XML_responses = XML_responses
    return new_XML_responses

@st.cache_data
def get_metamodel_response(XML_responses, llm_selected, metamodels_to_process):
    new_text_value = []
    i=0
    for XML_fragment in XML_responses:
        i+=1
        new_text_value.append(metamodelAndRAG.metamodel_operations(XML_fragment, i, metamodels_to_process, llm_selected))
    return new_text_value

new_XML_responses = cache_XML_responses(XML_responses)


#st.write(new_XML_responses)
if format_chosen == "legalruleml":


    widget_id = (id for id in range(1, 8))

    key_id = str(next(widget_id))
    key_id_1 = "condn" + str(key_id)
    key_id_6 = "finalwrite" + str(key_id)
    input_for_metamodel = st.radio(
        'Do you want to align with the metadata model? Enter "Yes" to continue with metamodel alignment or "No" to continue without doing so', ["No", "Yes"], key = key_id_1)

    if input_for_metamodel == "Yes":
        metamodels_to_process=metamodel_options(key_id)
        tweaked_XML = get_metamodel_response(XML_responses, llm_selected, metamodels_to_process)
    else:
        tweaked_XML = XML_responses

    st.write(tweaked_XML, key=key_id_6)

    new_XML_responses = cache_XML_responses(tweaked_XML)

    XML_responses = new_XML_responses

else:
    st.write("This page only loads if you have selected 'legalruleml' as the option for generation")


