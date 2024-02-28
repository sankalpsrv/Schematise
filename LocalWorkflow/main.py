import sys
import os
import pandas as pd
import utils
import seconddraftCombinedProcess

def main():
    directory = "./_cache"

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
    df2 = utils.csv_parser()
    XML_responses = seconddraftCombinedProcess.responseGetter(df2, XML_arg="", num_interval)

    with open("FinalXML.txt", "w") as filename:
        filename.write(str(XML_responses))


if __name__ == "__main__":
    main()


