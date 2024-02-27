# Important: This is in-development, only for internal use amongst mentors.

Features currently implemented:
1. XML generation by prompting every section with the context of a few-shot-template.
2. Automatic metamodel alignment (automatically aligning with all 7 metamodels utilised in this program)
3. Manual metamodel alignment (by specifying which of the 7 metamodels and the order you want to align the XML with them in)

### How to run:

0. Run the following command or download the ZIP file for the "dev" branch - `git clone -b dev https://github.com/sankalpsrv/Schematise.git`
1. Change directory to "Azure Workflow" and install the requirements (preferably in a virtual environment) using - `pip install -r requirements27th.txt`
2. Download the sections you want and put them in the format of two columns representing "Section Title" and "Nested Content" with the latter containing all the nested contents inside the Section Title. For reference, see the E-waste rules parsed in this format, as "fullsections.csv"
3. Specify the range of sections you want to run in utils.csv_parser (at line number 14) - defaulted to Sections 71-73
4. Put in your Azure endpoint URL and api_key for the Llama Chat 7b model at lines 369-371 and 415-417 of `model.py`
5. Run main.py with the argument --xmlh (for manual metamodel alignment) and --xmla (for automatic metamodel alignment)
6. Specify the interval at which you want the sections for which the XML is generated successively to be aligned when prompted for the same.

### Need to implement the entire program on a local machine, hence the current code will undergo changes 


### Goal for the workflow 

<img src = "./Flowchart.png">
