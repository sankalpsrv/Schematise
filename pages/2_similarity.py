import streamlit as st
import pandas as pd
import numpy as np
import model, metamodelAndRAG, combinedProcess, utils
#from Schematise import XML_responses, format_chosen
from xml.etree.ElementTree import ParseError  # Import ParseError from the XML parsing library you're using
import traceback

XML_responses = st.session_state['XML_resp']
format_chosen = st.session_state['fchosen']
llm_selected = st.session_state['llmc']

condition_similarity_check = st.radio("Do you want to check for similarities? Enter Yes or No",
         ["Yes", "No"])
widget_id_2 = (id for id in range(1, 100))

if condition_similarity_check == "Yes":
    # Generate a unique key ID for this session or interaction
    key_id_sim = str(next(widget_id_2))  # Consider revising this approach for simplicity
    key_id_7 = "index" + key_id_sim

    # Taking two index numbers as input from the user
    index_numbers = st.text_input("Please enter two index numbers (separated by space) you would like to view/confirm for comparison", key=key_id_7)

    if index_numbers:  # Proceed only if the user has entered something
        indexes = index_numbers.split()
        if len(indexes) == 2:
            try:
                index1, index2 = int(indexes[0]), int(indexes[1])

                # Creating or updating the key_id_indexes dictionary
                key_id_indexes = {}
                key_id_indexes[index1] = f"index_{index1}_{key_id_sim}"
                key_id_indexes[index2] = f"index_{index2}_{key_id_sim}"

                # Creating or updating the dict_compare dictionary
                dict_compare = {}
                dict_compare[int(key_id_sim)] = XML_responses[index1]
                dict_compare[int(key_id_sim)+1] = XML_responses[index2]
                key_id_8 = "table" + key_id_sim
                st.table(dict_compare)

                key_id_9 = "verifytable" + key_id_sim
                verify = st.radio("Do you want to check the above two XML segments for similarities? Enter Yes or No",
                                  ["Yes", "No"], key=key_id_9)
                if verify == "Yes":

                    similarities_dict_above_threshold = utils.XML_Similarity(dict_compare[int(key_id_sim)], dict_compare[int(key_id_sim)+1])
                    key_id_10 = "listofsim" + key_id_sim
                    st.write(
                        "These are the list of similarities between the newest XML generation and the previously generated XML with their index numbers: \n",
                        key=key_id_10)
                    i = 0
                    for XML_values, similarity in similarities_dict_above_threshold.items():
                        key_id_indexes_2 = {}
                        key_id_indexes_2[i] = f"index_sim_compare_{i}_{key_id_sim}"

                        st.write(i, ".: Similarity between the two XML elements or attributes here", XML_values,
                                 "is equal to", similarity, key=key_id_indexes_2[i])
                        i += 1

                else:
                    pass
            except ValueError:
                st.error("Please enter valid integer index numbers.")
            except ParseError as e:
                tback = traceback.format_exc()
                key_error = "XMLerror" + key_id_sim
                key_replacement = "XMLreplacement" + key_id_sim
                key_upload = "XMLupload" + key_id_sim
                if tback.find("dict1") is not -1:
                    tback_file = "First XML segment selected"
                    tback_input = XML_responses[int(indexes[0])]
                elif tback.find("dict2") is not -1:
                    tback_file = "Second XML segment selected"
                    tback_input = XML_responses[int(indexes[1])]
                st.write(f"The following error occured: {e} {tback}", key=key_error)
                XML_replacement = st.text_input("Please replace the following XML segment or upload a file", f"{tback_input}", key=key_replacement)
                uploaded_file = st.file_uploader(f"Alternatively, you can upload a corrected file in place of {tback_file} that corrects the error", key=key_upload)

                if uploaded_file is not None and tback_file == "First XML segment selected":
                    XML_responses[int(indexes[0])] = (uploaded_file.read()).decode("utf-8")
                elif uploaded_file is not None and tback_file == "Second XML segment selected":
                    XML_responses[int(indexes[1])] = (uploaded_file.read()).decode("utf-8")
                elif uploaded_file is None and tback_file == "First XML segment selected":
                    XML_responses[int(indexes[0])] = XML_replacement
                elif uploaded_file is None and tback_file == "Second XML segment selected":
                    XML_responses[int(indexes[1])] = XML_replacement

                st.session_state['XML_resp'] = XML_responses
