import model
import metamodelAndRAG
import utils

import json
import streamlit as st
global_openai_key = ''
def responseGetter(openai_key, df2, llm, format_chosen):

    global global_openai_key
    global_openai_key= openai_key

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

        #result = '' # Accounting for instances where empty output has been generated
        #while not result or len(result) < 250:
        result = model.send_request(openai_key, section_for_conversion, llm, format_chosen)


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



