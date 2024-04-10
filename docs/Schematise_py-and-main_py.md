# main.py and Schematise.py

## Table of Contents

1. Introduction
2. "import" statements
3. Functions 
4. Checklist of features across Streamlit and LocalWorkflow

### 1. Introduction

#### Schematise.py

This is used in the Streamlit version of the app to create a GUI interface, currently hosted on schematise.streamlit.app.

#### main.py
This is used in the LocalWorkflow to create a CLI interface for the application.
The LocalWorkflow, most notably implements a HuggingFacePipeline, which can be used to run the application on models that don't pose restrictions on utilisation for creation of datasets.

### 2. "import" statements or dependencies

- .env file with IK API Key and Open AI Key if needed

### 3. Functions and classes

#### Schematise.py - main()

- creates the app's main page which allows users to:
  - pass their IndianKanoon key or upload the CSV file
    - If IndianKanoon is selected, pass the document number
- Allows user to specify which format they want (LegalRuleML or LegalDocML)
- Specify if a certain range of the csv file is to be converted only
- Allows users to see a dataframe for the range selected
- Writes the XML generated in .TXT format for the user
  - This allows the user to verify the XML on their own
- Passes all the required values by other pages in the app to the session variables

#### Schematise.py - set_env(), load_data()

- used to create a cache of the data which is created or stored by these functions
  - For environment variables holding the IK API key and OpenAI Key, so that user does not have to re-enter them
  - and for the dataframe selected

#### Schematise.py - get_XML()

- makes the call to combinedProcess.py for generating the XML at the backend

####  main.py - main()

- Part of the LocalWorkflow
- Creates a workflow that prompts user for each of the conditions they want to be implemented
- Asks user for document number, if IndianKanoon is selected, and thereafter creates a csv file out of the sections in a  standard format.
- passes the csv_file created to utils.csv_parser
- XML_arg and num_interval are still in progress, and are intended to contain the parameters for metamodel alignment if required.



### 4. Checklist of features across formats

(TBD = To Be Developed)

| Feature                           | Streamlit | LocalWorkflow | LegalDocML         | LegalRuleML |
|-----------------------------------|-----------|---------------|--------------------|-------------|
| OpenAI option                     | Yes       | Yes           | Yes                | Yes         |
| IndianKanoon option               | Yes       | Yes           | Yes                | Yes         |
| CSV upload option                 | Yes       | Yes           | Yes                | Yes         |
| Download XML file                 | Yes       | Yes           | Yes                | Yes         |
| Dataframe viewing after selection | Yes       | No            | Yes (in Streamlit) | Yes (in Streamlit) |
