# Complianalyse
An automated regulatory mapper for Indian laws

## Problem
Lawyers and indeed even laypersons often have to peruse statutes with the aim of identifying requirements, rights and obligations specific to their business function/purpose.

## Proposed solution
### For end users
To provide users with a list of compliance checklists for their user function specific to the enactment and user function they select/provide. 
### As reuasable code
Considering that LegalRuleML exists as a solution to encode legal statutes into text, reference will be made to (part of) its schema for generating the categories for classification. I will do so by utilising an LLM based approach to generate an initial categorisation of obligations only, similar to what is described in [this paper](https://scholar.google.com/scholar?cluster=14104070510978091644&hl=en&as_sdt=0,5). 

### Features

- Checklist will be relative to the specific user/function they select (encoded as "Agent" in the LegalRuleML format)
- Point in time classification for those aspects of the law which have undergone changes over time so as to provide users a temporal data for the laws that they provide.
- Knowledge graphs will be generated from the XML schema using either the same LLM and in-context learning or parallelly exploring Python libraries for the [same](https://github.com/Accenture/AmpliGraph)

### Ethical considerations

- App shall provide a disclaimer before executing and at the generated results in each case regarding the results not constituting legal advice.
- No user data will be sought or stored in any place. The database integration will store the inference results for each statute regardless of user function ("Agent") selected

# Roadmap

1. Comparing the fine-tuning approaches to LLM for their resource and performance capabilities
  - In-context learning for prompts that generate the LegalRuleML schema. This has already shown some results. [Link to ChatGPT prompts that generated results (will replicate further with programmatic access)](https://chat.openai.com/share/04a01b6f-7829-4765-84f8-9038e9d68666)
  - LoRA adaptation using either HuggingFace or Lit-GPT as outlined [here](https://cameronrwolfe.substack.com/p/easily-train-a-specialized-llm-peft). This will use the training on a custom-generated dataset. Since In context learning has already shown some results, this will be used to create a dataset for some Environmental Laws (owing to the extensive compliance requirement there, which I have [previously researched on](https://sankalpsrv.in/2021/08/15/dissertation/).

2. Once the backend is developed to the extent that it is accurately generating the schema, the next step will be to integrate with access to laws. The most feasible option is the IndianKanoon API as it has a standard format for laws that are compliant with the Akoma Ntoso format.

3. Thereafter, building the front-end, most likely in the form of a Flask app that allows users to select a statute or rule/regulation via a search bar. Once the page is loaded with the statute, it will allow users to select a user function ("Agent" in LegalRuleML terms) and open a sidebar with the options to view a graded list of compliances and a link to generate knowledge graphs in an interactive manner.

4. Lastly, to save inference costs, integrations with PostgreSQL for the cached versions of laws will be stored in the working directory itself.

### LLMs being compared

Most of these will be tested on my CPU. However, if need arises HuggingFace's Inference API might be made use of.

- LegalBert
- InLegalBert
- Llama
- GPT

# TO-DOs

[] Make a draft version of the app for review at the Hackday which will work on a representative set and generate compliances in Markdown/Text format.

[] Test different LLMs described in the section above for their accuracy. Share results in separate folder as Jupyter Notebooks.

[] Work on representing knowledge graphs, and identify further Natural Language Processing tasks. 

[] Identify a way to benchmark or validate the performance of an LLM.

[] Draft a disclaimer for the app to show users.

[] Select copyright license.

# Progress

- Was able to test the few-shot learning in-context learning approach via LangChain and OpenAI. Due to token limits on LangChain, using a split approach was necessary.
- Nevertheless, was able to generate LegalRuleML code via this approach - [available in this notebook (click here)](https://github.com/sankalpsrv/Complianalyse/blob/main/LangChain_FewShot.ipynb)
