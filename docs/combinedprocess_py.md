# combinedProcess.py

## Table of Contents

1. Introduction
2. "import" statements
3. Functions 
4. Checklist of features across Streamlit and LocalWorkflow

### 1. Introduction

Collects the response from a call to [model.py](./model_py.md) and adds further processing where needed.

### 2. "import" statements

[To be completed]

### 3. Functions and classes
#### responseGetter(openai_key, df2, llm, format_chosen)

- Iterates through each row of the dataframe passed to it as a parameter 'df2' and passes it to the [model.py](./model_py.md)
- Prepends the LegalRuleML and LegalDocML namespace to the start of the XML generated and appends it with the relevant closing tag
- Joins each XML response into a ".txt" document.

#### metamodel_options()

- implemented as a part of [metamodelandRAG.py](./metamodelAndRAG_py.md) for the STreamlit app through a GUI
- allows users to choose between the 7 available metamodel definitions and RFD files for aligning their XML output more accurately with the XML output generated.
- creates an interface that terminates when users press enter
- returns the list of metamodel options selected by the user

#### similarityProcess

- implemented in a separate page in Streamlit app
- Seeks to get list of similarities between XML tags and their attributes from [utils.py](./utils_py.md)
- Allows user to upload corrected file in case of similarities detected
- For the Local Workflow, it is a WIP, no calls are made to it currently
### 4. Checklist of features across formats

| Feature                           | Streamlit                                 | LocalWorkflow                        | LegalDocML | LegalRuleML |
|-----------------------------------|-------------------------------------------|--------------------------------------|------------|-------------|
| Metamodel alignment interface     | Not in this module, but otherwise present | Yes                                  | No         | Yes         |
| Namespace and closing tag adition | Yes                                       | Yes                                  | Yes        | Yes         |
| Metamodel option selection        | Yes (one at a time), but in a separate module | Yes, multiple, and in order selected | No         | Yes         |

