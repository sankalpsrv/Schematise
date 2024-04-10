# metamodelAndRAG.py

## Table of Contents

1. Introduction
2. "import" statements
3. Functions 
4. Checklist of features across Streamlit and LocalWorkflow

### 1. Introduction

The functionality for metamodel tweaking using RAG has been isolated in this python file for the purpose of creating further modifications when required to this part of the process.
This function is present in both Streamlit and LocalWorkflow versions.

### 2. "import" statements

[To be completed]

### 3. Functions and classes

#### class CustomRetriever(BaseRetriever):

- a self-querying CustomRetriver that is utilised to extract data from a list of metamodel definitions and example RDF files

#### getRAG_metamodels(openai_key, text_value, metamodel_number):

- extracts the metamodel from the CustomRetriever Object
- makes a call to model.py's RAGPrompt function that handles the model request functionality
- Currently, it is very resource consuming on the HuggingFacePipeline in the LocalWorkflow, hence it is preferred not to use this
- WIP: In future, it is intended to implement one of the Vectorstore retrievers available within the LangChain framework, which might require OpenAI key

#### metamodel_operations(openai_key, text_value, i, metamodels_to_process, llm_selected="OpenAI"):

- creates the interface between the combiendProcess and metamodelAndRAG files
- stores the output from metamodel alignment in the working directory

### 4. Checklist of features across formats

(TBD = To Be Developed)

| Feature           | Streamlit | LocalWorkflow                  | LegalDocML | LegalRuleML |
|-------------------|-----------|--------------------------------|------------|-------------|
| Self-Querying RAG | Yes       | Yes                            | No         | Yes         |
| HuggingFaceOption | No        | Difficult (resource-intensive) | No         | Yes         |
| VectorStore RAG   | TBD       | TBD                            | TBD        | TBD         |
