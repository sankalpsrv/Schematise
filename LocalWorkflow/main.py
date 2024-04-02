import sys
import os
import pandas as pd
import utils
import seconddraftCombinedProcess
from decouple import config
import IK_templates

def main():
    directory = "./_cache"

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    option = input("Enter 0 to use IndianKanoon or any other key to provide a csv file \n")

    if option == "0":
        ik_api = config('IK_API_KEY')

        docnumber = input("Specify a document number to get from IndianKanoon \n")

        IK_templates.extract_text(docnumber, ik_api)

        filename = "sections"

    else:
        filename = input ("What is your CSV file containing sections named? (without the extension \n")

    csv_filename = filename + ".csv"

    option_model = input ("Enter 0 to use OpenAI or any other key to use Llama2-7b-chat on your local machine \n")

    if option_model == "0":
        llm = "OpenAI"
    else:
        llm = "HuggingFace"


    option_format = input("Enter 0 to generate LegalRuleML or any other key to generate LegalDocML \n")

    if option_format == "0":
        format_chosen = "legalruleml"
    else:
        format_chosen = "legaldocml"

    df2 = utils.csv_parser(csv_filename, df_condition="0")
    XML_responses = seconddraftCombinedProcess.responseGetter(df2, XML_arg="", llm = llm, format_chosen = format_chosen, num_interval="5")

    with open("FinalXML.txt", "w") as filename:
        filename.write(str(XML_responses))


if __name__ == "__main__":
    main()


