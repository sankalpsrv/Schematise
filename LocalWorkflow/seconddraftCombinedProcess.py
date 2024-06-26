import model
import metamodelAndRAG
import utils

import json

def responseGetter(df2, XML_arg, llm = "OpenAI", format_chosen = "legaldocml", num_interval = 5):


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
            model.instantiate_model()
            result = model.send_request(section_for_conversion, llm, format_chosen)

        filename = f"_cache/section_{i}"
        with open(filename, "w") as fn:
            fn.write(str(result))

        # result_json = json.loads(result)

        # Extract the codeblock
        # text_value_old = result_json['choices'][0]['message']['content']
        text_value = utils.strip_code_block(result)
        filename_debug_old = "./_cache/old_text_value_" + str(i) + ".txt"
        filename_debug_stripped = "./_cache/text_value_stripped_" + str(i) + ".txt"
        with open(filename_debug_old, "w") as fn:
            fn.write(result)
        with open(filename_debug_stripped, "w") as fn:
            fn.write(text_value)

        if llm == 'OpenAI':
            new_text_value = result
        else:
            new_text_value = text_value
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

    joined_XML_responses = string_namespace + '\n'.join(XML_responses) + string_end

    return joined_XML_responses


## The following two functions metamodel_options and similarityProcess - are for future integration
def metamodel_options():

    metamodels_to_process = []
    print(
        "The following metamodels can be used to align the new XML generation: (Input anything other than integers 1-7 to continue")

    print(
        "1. Context \n 2. Defeasible \n 3. Deontic \n 4. Legal Temporal \n 5. Metadata-actor \n 6. Metadata jurisdiction authority \n 7. Statement")

    while True:
        metamodel_selected = input(
            'Enter the number of the metamodel to process (or press enter to continue with all/selected): ')

        # Break the loop if the input is not an integer between 1 and 7 or if it's an empty string
        if not metamodel_selected.isdigit() or int(metamodel_selected) not in range(1, 8):
            if metamodel_selected == "":
                break  # Exit the loop if the user just presses enter
            print("Invalid input. Please enter a number between 1 and 7, or press enter to finish.")
            continue  # Prompt the user again for a valid input

        # If the input is valid, add it to the list of metamodels to process
        metamodels_to_process.append(metamodel_selected)

    return metamodels_to_process

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
            new_text_value = metamodelAndRAG.metamodel_operations(text_value, metamodels_to_process)
            return new_text_value
        else:
            return text_value


