# model.py

## Table of Contents

1. Introduction
2. "import" statements
3. Functions 
4. Checklist of features across Streamlit and LocalWorkflow

### 1. Introduction

- Implements LangChain 
  - for implementing example selection, prompting, LLMChain, and more.
  - Reason - This makes the development capable of expanding on a FOSS framework which increases mutability (such as between choice of LLMs)

### 2. "import" statements

[To be completed]

### 3. Functions and classes
#### Global variables

- hf_global | global scope | used to store HuggingFacePipeline object
- llm_global | global scope | stores choice of llm - either OpenAI or 

#### CustomExampleSelector
- class created on the basis of LangChain documentation for creating a kind of self-querying retriever
- takes the format chosen as the "input_variable" and depending on that returns the examples to be used in the RAG Chain

#### instantiate_model

- reads the value in llm_global
- creates a huggingface object for the transformer pipeline (in case of LocalWorkflow only) or returns an OpenAI chain

#### send_request

- forms the interface for passing the prompts to the chat models for output
- constructs a chat prompt template using the format chosen and by creating an object of the CustomExampleSelector class
- passes the chat prompt template to an LLMChain
  - Reason - can be used to create more complex RAG Chains in the future

#### RAGPrompt

- Runs a system prompt which contains the definition as well as extract of a metamodel from the LegalRuleML documentation
- Filters through a list of metamodel definition and XML through a custom Retriever object which is a self-querying retriever made using LangChain's example for [CustomRetriever class](https://python.langchain.com/docs/modules/data_connection/retrievers/)
- input_dict is a dictionary that contains the XML  for alignment with the metamodel.

### 4. Checklist of features across formats

(TBD = To Be Developed)

| Feature | Streamlit | LocalWorkflow | LegalDocML | LegalRuleML |
| ------- |-----------|---------------|------------|-------------|
| OpenAI option | Yes       | Yes           | Yes        | Yes         |
| HuggingFaceOption | No        | Yes           | Yes        | Yes         |
| Metamodel | Yes       | Yes           | No         | Yes         |
| Example selection | Yes       | Yes           | TBD        | TBD         |