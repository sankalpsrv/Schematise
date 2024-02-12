# Schematise (formerly "Complianalyse")
### Submission to [The Fifth Elephant's Open Source AI Hackathon](https://hasgeek.com/fifthelephant/open-source-ai-hackathon/)
An LLM enabled schema generator for statutes in the LegalRuleML format. 

While originally meant as a compliance mapper, this project's author, guided by the [Unix philosophy of "Doing one thing and doing it well"](https://en.wikipedia.org/wiki/Unix_philosophy) has decided to focus on creating something more modular, rather than focus on a single use-case. Accordingly, repository details have been amended with struck out text where it was only applicable to the previous approach. 

# How to run (proof of concept version)

### Requirements

- OpenAI Key (make an account on openai.com and get keys https://platform.openai.com/api-keys)
- IndianKanoon API Key (sign up and obtain key via https://api.indiankanoon.org)

1. Install python.
2. (Optional) Create virtual environment - `virtualenv complianalyse`
   `source /complianalyse/bin/activate` 
3. Install requirements via txt file `pip install -r requirements.txt`
4. run `python main.py` and follow steps
   


## Problem
Lawyers and indeed even laypersons often have to peruse statutes with the aim of identifying requirements, rights and obligations specific to their business function/purpose.

## Proposed solution
~### For end users~
~To provide users with a list of compliance checklists for their user function specific to the enactment and user function they select/provide.~
~### As reuasable code~
Considering that LegalRuleML exists as a solution to encode legal statutes into text, reference will be made to its schema for generating the categories for classification. I will do so by utilising an LLM based approach to generate ~an initial categorisation of obligations only,~ an entire statute's schema similar to what is described in [this paper](https://scholar.google.com/scholar?cluster=14104070510978091644&hl=en&as_sdt=0,5).

### Features

~- Checklist will be relative to the specific user/function they select (encoded as "Actor" in the LegalRuleML format)~
~- Point in time classification for those aspects of the law which have undergone changes over time so as to provide users a temporal data for the laws that they provide.~
~- Knowledge graphs will be generated from the XML schema using either the same LLM and in-context learning or parallelly exploring Python libraries for the [same](https://github.com/Accenture/AmpliGraph)~

- Users can upload text files/pdfs and download schema in XML format.
- Will allow users to specify parts of the Schema they wish to have consistency in, such as the XML tags for certain terms which are repeated throughout the statute.
- Users will be able to use either OpenAI, prompt-engineering, RAG, or a fine-tuned model, since each can generate different outputs and have different inference costs. 


### Ethical considerations

- App shall provide a disclaimer before executing and at the generated results in each case regarding the results not constituting legal advice.
- No user data will be sought or stored in any place. The database integration will store the inference results for each statute ~regardless of user function ("Agent") selected~

# Roadmap

1. Develop a script that can take laws in text or PDF format and divide them by sections.
  - This can include LLM based text-classification, however (see next point)
  - For a few standardised formats, this script should be able to do it without reliance on an LLM.
2. Implementing different LLM based text-generation approaches (list is indicative at this point)
  - In-context learning for prompts that generate the LegalRuleML schema. This has already shown some results. [Link to ChatGPT prompts that generated results (will replicate further with programmatic access)](https://chat.openai.com/share/04a01b6f-7829-4765-84f8-9038e9d68666)
  - Implement an approach that uses RAG, by processing the documentation provided for LegalRuleML. 
  - LoRA adaptation using either HuggingFace, [Axolotl](https://github.com/OpenAccess-AI-Collective/axolotl) or Lit-GPT as outlined [here](https://cameronrwolfe.substack.com/p/easily-train-a-specialized-llm-peft).
  - Also will perform the training of a fine-tuned model on a custom-generated dataset, using an LLM model that allows for using its output for training (for e.g., OpenAI does not). Since In context learning has already shown some results, this will be used to create a fine-tuning dataset for some Environmental Laws (owing to the extensive compliance requirement there, which I have [previously researched on](https://sankalpsrv.in/2021/08/15/dissertation/).

3. ~Once the backend is developed to the extent that it is accurately generating the schema, the next step will be to integrate it with access to laws. The most feasible option is the IndianKanoon API as it has a standard format for laws that are compliant with the Akoma Ntoso format.~ Upload the models to huggingface and run benchmarking tests for it on a repeated basis in order to identify whether further fine-tuning is required and to what extent.

4. ~Thereafter, building the front-end, most likely in the form of a Flask app that allows users to select a statute or rule/regulation via a search bar. Once the page is loaded with the statute, it will allow users to select a user function ("Actor" in LegalRuleML terms) and open a sidebar with the options to view a graded list of compliances and a link to generate knowledge graphs in an interactive manner.~ Compare each of the approaches and select a default approach, as well as integrate each approach into the application.

5. Lastly, to save inference time, integrations with PostgreSQL/sqlite for the cached versions of laws will be stored in the working directory itself.

### LLMs being compared

~Most of these will be tested on my CPU. However, if need arises~ HuggingFace's Inference API will be made use of, in addition to Azure or any other comparable compute resources provider.

- LegalBert
- InLegalBert
- Llama
- GPT

# TO-DOs

[x] Make a draft version of the app for review at the Hackday which will work on a representative set and generate compliances in Markdown/Text format.

[] Find a teammember before 15th.

[] Update project page on hasgeek continuously. 

[] Identify the correct chunking strategy for RAG. Share approaches as notebook.

[] Test different LLMs described in the section above for their accuracy. Share results in separate folder as Jupyter Notebooks.

[] Upload the models as fine-tuned models once satisfactory performance is achieved.

~Work on representing knowledge graphs, and identify further Natural Language Processing tasks.~

[] Identify a way to benchmark or validate the performance of an LLM.

[] Draft a disclaimer for the app to show users.

[] Select copyright license.

# Progress

- Was able to test the few-shot learning in-context learning approach via LangChain and OpenAI. Due to token limits on LangChain, using a split approach was necessary.
- Nevertheless, was able to generate LegalRuleML code via this approach - [available in this notebook (click here)](https://github.com/sankalpsrv/Complianalyse/blob/main/LangChain_FewShot.ipynb)
- The test output generated for the entire Bio-medical Waste Rules is here - [testbmw.txt](https://github.com/sankalpsrv/Complianalyse/blob/main/src/testbmw.txt)
- This was generated using the script in the ["src" folder of this repository (click here)](https://github.com/sankalpsrv/Complianalyse/blob/main/src/main.py)
