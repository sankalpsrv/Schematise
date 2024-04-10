# utils.py

## Table of Contents

1. Introduction
2. "import" statements
3. Functions 
4. Checklist of features across Streamlit and LocalWorkflow

### 1. Introduction

This contains a set of utility functions that are necessary to be invoked across various modules in the app.

### 2. "import" statements

- thefuzz 
  - Used for calculating SimpleRatio
- pandas
  - Used to create dataframe out of CSV file
- xml.etree
  - For parsing the contents of the XML file

### 3. Functions and classes

#### csv_parser(filename, start_value=70, end_value=73)

- creates a dataframe using pandas
- range can be specified by setting df_condition to "1"

#### find_last_closing_tag_index(xml_string)

- finds the last closing tag '>' to strip the code block from the XML output generated

#### strip_code_block(string)

- Used in LocalWorkflow and with HuggingFacePipeline
- extracts the XML output from the entire chat response of the LLM
- This ensures that XML_operations such as similarity processing and checking for general validity can be conducted even when using the LocalWorkflow

#### XML_Similarity(XML_responses, text_value)

- takes two XML files, depending on the index numbers chosen by the user from the dataframe
- creates a dictionary of elements and attributes
- calculates the similarity between each element and attribute from each of the XML files, comparing both elements and attributes of each file with each other.
  - Reason: In the absence of consistency amongst similarly generated XML tags across various iterations, they are compared so that user can change serialisation of the numbering if it occurs across various tags
- WIP: It may be necessary to allow user to view and select each XML portion as per their preference, or check throughout the document
- Currently implemented only in Streamlit GUI

### 4. Checklist of features across formats

(TBD = To Be Developed)

| Feature                | Streamlit | LocalWorkflow | LegalDocML | LegalRuleML |
|------------------------|-----------|---------------|------------|-------------|
| Dataframe generation   | Yes       | Yes           | Yes        | Yes         |
| strip_code_block       | No        | Yes           | Yes        | Yes         |
| XML_similarity testing | Yes       | TBD           | Yes        | Yes         |
