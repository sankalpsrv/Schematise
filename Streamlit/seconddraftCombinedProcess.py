import model
import metamodelAndRAG
import utils

import json
import streamlit as st
def responseGetter(df2, llm, format_chosen):


    XML_responses = []
    if format_chosen == "legalruleml":
        string_namespace = '<LegalRuleML xmlns:lrml="http://www.oasis-open.org/committees/legalruleml" xmlns:ruleml="http://www.oasis-open.org/committees/legalruleml">'
        string_end = "</LegalRuleML>"
    else:
        string_namespace = '<akomaNtoso>'
        string_end = "</akomaNtoso>"
    i = 0

    for index, row in df2.iterrows():
        section_title = row['Section Title']
        nested_content = row['Nested Content']

        i+=1

        # Process section_title and nested_content as needed
        # print(f"Section Title: {section_title}")
        # print(f"Nested Content: {nested_content}\n")
        section_for_conversion = f"{section_title}: {nested_content}\n"

        result = '' # Accounting for instances where empty output has been generated
        while not result or len(result) < 250:
            result = model.send_request(section_for_conversion, llm, format_chosen)


        filename = f"_cache/section_{i}"
        with open(filename, "w") as fn:
            fn.write(str(result))

        #result_json = json.loads(result)

        # Extract the codeblock
        #text_value_old = result_json['choices'][0]['message']['content']
        text_value = utils.strip_code_block(result)
        filename_debug_old = "./_cache/old_text_value_" + str(i) + ".txt"
        filename_debug_stripped = "./_cache/text_value_stripped_" + str(i) + ".txt"
        with open(filename_debug_old, "w") as fn:
            fn.write(result)
        with open(filename_debug_stripped , "w") as fn:
            fn.write(text_value)

        if llm == 'OpenAI':
                new_text_value = string_namespace + result + string_end
        else:
                new_text_value = string_namespace + text_value + string_end
        # This code has been removed due to the process taking more memory on a Local Deployment than available
        '''elif i % int(num_interval) == 0 or i == 3:
            if XML_arg == "--xmla":
                new_text_value = metamodelAndRAG.metamodel_operations(text_value, i)
            elif XML_arg == "--xmlh":
                metamodels_to_process = metamodel_options()
                new_text_value = metamodelAndRAG.metamodel_operations(text_value, i, metamodels_to_process)
        '''


        XML_responses.append(new_text_value)
        print (f"XML structure on the number {i} iteration is as follows: \n{XML_responses}")

    return XML_responses



def similarityProcess(XML_responses, text_value, similarities_dict_below_threshold):
    print(
        "These are the list of similarities between the newest XML generation and the previously generated XML with their index numbers: \n")
    i = 0
    for XML_values, similarity in similarities_dict_below_threshold.items():
        i += 1
        print(i, ".: Similarity between the two XML elements or attributes here", XML_values, "is equal to", similarity)

    input_for_revision_opt = input(
        'Do you want to upload an entire new revised XML in place of the newest XML generation? Enter "Yes" or input any other key to continue')

    if input_for_revision_opt == "Yes":
        new_text_value_fn = input('Enter the filename')

        with open(new_text_value_fn, "r") as new_text_file:
            new_text_value = new_text_file.read()
        return new_text_value

    else:
        input_for_metamodel = input('Do you want to align with the metadata model? Enter "Yes" or enter any other key to continue without doing so')

        if input_for_metamodel == "Yes":
            metamodels_to_process=metamodel_options()
            print(metamodels_to_process)
            new_text_value = metamodelAndRAG.metamodel_operations(text_value, metamodels_to_process)
            return new_text_value
        else:
            return text_value





