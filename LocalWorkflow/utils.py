import pandas as pd
import xml.etree.ElementTree as ET
from thefuzz import fuzz
import re
def csv_parser(filename, df_condition = "0"):

    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(filename)

    if df_condition == "1":
        df2 = df.iloc[0:3]
    else:
        df2=df.copy()

    return df2



def find_last_closing_tag_index(xml_string):
    # Regular expression to match closing XML tags
    pattern = r'<\/.*>'

    # Find all occurrences of the closing tags
    matches = list(re.finditer(pattern, xml_string))

    # Check if there are any matches
    if matches:
        # Get the last match
        last_match = matches[-1]
        # Return the start index of the last closing tag
        return last_match.end()
    else:
        # Return an indication that no closing tag was found
        return -1
def strip_code_block(string):
    #Find the first occurrence of ```
    start_index = string.find('```')
    end_index = len(string)
    no_start_index = False
    no_end_index = False
    if start_index == -1:
        no_start_index = True # No code block found
        start_index = 0
    else:
        start_index += 3

    # Find the next occurrence of ``` after the first one
    end_index = string.find('```', start_index + 3)
    if end_index == -1:
        no_end_index = True
        end_index = len(string)# No closing code block found
    else:
        pass

    # Extract the part between the first and last ```
    extracted_string = string[start_index:end_index]


    #extracted_string = string
    # Find the index of the first occurrence of '<' after removing the code block
    index_of_first_opening_bracket = extracted_string.find('<')

    # Find the index of the last closing bracket
    index_of_last_closing_bracket = find_last_closing_tag_index(string)

    # Extract the part of the string between the first opening '<' and the last closing '>'
    if index_of_first_opening_bracket != -1 and index_of_last_closing_bracket != -1:
        result = extracted_string[index_of_first_opening_bracket -1:index_of_last_closing_bracket +1]
    elif index_of_first_opening_bracket != -1 and index_of_last_closing_bracket == -1:
        result = extracted_string[index_of_first_opening_bracket -1:]
    elif index_of_first_opening_bracket != -1 and index_of_last_closing_bracket != -1:
        result = extracted_string[:index_of_last_closing_bracket+1]
    else:
        result = extracted_string

    return result



def XML_Similarity(XML_responses, text_value):

    def get_elements_and_attributes(xml_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        elements_and_attributes = {}

        # Function to recursively traverse the XML tree
        def traverse(element):
            nonlocal elements_and_attributes

            # Adding the element itself
            attributes = element.attrib

            elements_and_attributes[element.tag] = list(element.attrib.keys())
            for attr in attributes:
                attributes_with_values = (attr, attributes.get(attr, 0))

                elements_and_attributes[element.tag] = attributes_with_values

            # Recursively traversing child elements
            for child in element:
                traverse(child)

        traverse(root)

        return elements_and_attributes


    def fuzzy_similarity(s1, s2):
        """
        Compute the fuzzy string similarity using TheFuzz library.
        """
        return fuzz.ratio(s1, s2) / 100.0  # Convert to a float [0, 1]

    def remove_string_from_tuple_value(value, string_to_remove):
        """
        Remove a specified string from all elements in the tuple value.
        """
        return tuple(item.replace(string_to_remove, '') for item in value)

    def clean_dictionary(dictionary, string_to_remove):
        """
        Remove a specified string from all keys and values in the dictionary.
        """
        cleaned_dict = {}
        for key, value in dictionary.items():
            cleaned_key = key.replace(string_to_remove, '')
            if isinstance(value, tuple):
                cleaned_value = remove_string_from_tuple_value(value, string_to_remove)
            else:
                cleaned_value = value.replace(string_to_remove, '') if isinstance(value, str) else value
            cleaned_dict[cleaned_key] = cleaned_value
        return cleaned_dict

    def compare_dicts(dict1, dict2, similarity_threshold=0.5):
        """
        Compare keys and values between two dictionaries and compute fuzzy similarity.
        """
        similarities_dict = {}
        for key1, value1 in dict1.items():
            for key2, value2 in dict2.items():
                # Compare key1 with key2
                key_similarity = fuzzy_similarity(key1, key2)
                #print(f"Similarity between key '{key1}' and key '{key2}': {key_similarity}")
                keypair_for_similarities_dict = key1 + '' + key2
                similarities_dict[keypair_for_similarities_dict]=key_similarity
                # Compare key1 with value2
                value_similarity_0 = fuzzy_similarity(key1, value2[0]) if isinstance(value2, tuple) else None
                value_similarity_1 = fuzzy_similarity(key1, value2[1]) if isinstance(value2, tuple) else None
                #print(f"Similarity between key '{key1}' and value '{value2[0]}': {value_similarity_0}")
                #print(f"Similarity between key '{key1}' and value '{value2[1]}': {value_similarity_1}")
                keypair_0_for_similarities_dict = key1 + '' + value2[0]
                keypair_1_for_similarities_dict = key1 + '' + value2[1]

                similarities_dict[keypair_0_for_similarities_dict]=value_similarity_0
                similarities_dict[keypair_1_for_similarities_dict]=value_similarity_1

            # Compare value1 with each key in dict2
            for key2 in dict2.keys():
                value_similarity_0 = fuzzy_similarity(value1[0], key2) if isinstance(value1, tuple) else None
                value_similarity_1 = fuzzy_similarity(value1[1], key2) if isinstance(value1, tuple) else None
                keypair_0_for_similarities_dict = key2 + '' + value1[0]
                keypair_1_for_similarities_dict = key2 + '' + value1[1]
                similarities_dict[keypair_0_for_similarities_dict]=value_similarity_0
                similarities_dict[keypair_1_for_similarities_dict]=value_similarity_1
                #print(f"Similarity between value '{value1[0]}' and key '{key2}': {value_similarity_0}")
                #print(f"Similarity between value '{value1[1]}' and key '{key2}': {value_similarity_1}")

            def remove_below_threshold(similarities_dict, similarity_threshold):
                return {key: value for key, value in similarities_dict.items() if value >= similarity_threshold}

            similarities_dict_below_threshold = remove_below_threshold(similarities_dict, similarity_threshold)

    def similarity_tweaking(similarities_dict_below_threshold, dict1, dict2_cleaned):



        value_to_tweak = input ("Press the index number of the similarities to tweak: ")

        print ("Which value do you prefer?")



    # Example usage
    xml_file_1 = './_cache/xml_file_1.xml'  # Replace with the path to your XML file
    xml_file_2 = "./_cache/xml_file_2.xml"
    combined_XML_responses = ' '.join(XML_responses)
    with open (xml_file_1, "w") as fn:
        fn.write(combined_XML_responses.replace('\n', ''))
    with open(xml_file_2, "w") as fn:
        fn.write(text_value)
    dict1 = get_elements_and_attributes(xml_file_1)
    dict2 = get_elements_and_attributes(xml_file_2)
    dict2_cleaned = clean_dictionary(dict2, "{http://www.oasis-open.org/committees/legalruleml}")
    similarities_dict_below_threshold = compare_dicts(dict1, dict2_cleaned)
    '''print(elements_and_attributes)
    for element, attributes in elements_and_attributes.items():
        print(f"Element: {element}")
        print(f"Attributes: {attributes}")
    '''


    return similarities_dict_below_threshold, dict1, dict2_cleaned

if __name__ == "__main__":
    #This section for debugging only

    df2 = csv_parser()
    print(df2)
