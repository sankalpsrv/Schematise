import sys
import os
import pandas as pd
import utils
import seconddraftCombinedProcess

def main(XML_arg, num_interval):
    directory = "./_cache"

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
    df2 = utils.csv_parser()
    XML_responses = seconddraftCombinedProcess.responseGetter(df2, XML_arg, num_interval)

    with open("FinalXML3.txt", "w") as filename:
        filename.write(str(XML_responses))


if __name__ == "__main__":
    XML_arg = sys.argv[1]
    print("XML_arg: ", XML_arg)
    if XML_arg == "--xmlh":
        option = "Manual"
    elif XML_arg == "--xmla":
        option = "Automatic"
    num_interval = input (f"You have chosen {option} metamodel alignment. \n Enter integer for specifying interval for metamodel alignment which is lesser than number of sections: \n")
    main(XML_arg, num_interval)


