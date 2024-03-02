# Schematise (formerly "Complianalyse")
### Submission to [The Fifth Elephant's Open Source AI Hackathon](https://hasgeek.com/fifthelephant/open-source-ai-hackathon/)
An LLM enabled XML generator for statutes in the Akoma Ntoso format. 

### [Go to "dev" branch (click here) to view more frequent development updates](https://github.com/sankalpsrv/Schematise/tree/dev)

# How to run (proof of concept version)

### Requirements

- OpenAI Key (make an account on openai.com and get keys https://platform.openai.com/api-keys)
- IndianKanoon API Key (sign up and obtain key via https://api.indiankanoon.org)

1. Install python.
2. (Optional) Create virtual environment - `virtualenv complianalyse`
   `source /complianalyse/bin/activate` 
3. Install requirements via txt file `pip install -r requirements.txt`
4. run `python main.py` and follow steps
   
# Progress

- Was able to test the few-shot learning in-context learning approach via LangChain and OpenAI. Due to token limits on LangChain, using a split approach was necessary.
- Nevertheless, was able to generate LegalRuleML code via this approach - [available in this notebook (click here)](https://github.com/sankalpsrv/Complianalyse/blob/main/LangChain_FewShot.ipynb)
- The test output generated for the entire Bio-medical Waste Rules is here - [testbmw.txt](https://github.com/sankalpsrv/Complianalyse/blob/main/src/testbmw.txt)
- This was generated using the script in the ["src" folder of this repository (click here)](https://github.com/sankalpsrv/Complianalyse/blob/main/src/main.py)
- Tested Llama through LangChain and AzureML Endpoints, found that it works via Azure, while LangChain presents some difficulties [click here to view notebook](https://github.com/sankalpsrv/Schematise/blob/main/Notebook-of-approaches/Llama2_AzureMl_CompletionsAPIAndChatAPI(1).ipynb)
- Tested Llama2-7b-chat on few shot prompting using the examples given in the [LegalRuleML documentation](https://github.com/sankalpsrv/Schematise/blob/main/Notebook-of-approaches/Llama_Documentation_Prompting.ipynb), found that it produces better output.
- Wrote a [set of functions that compare similarity scores for the XML file generated sequentially](https://github.com/sankalpsrv/Schematise/blob/main/Notebook-of-approaches/Similarity-XML-SimpleRatio.ipynb). This will be helpful for identifying places where there is overlap in case of Few-Shot Prompting.
- Wrote a [RAG approach using the metamodel and descriptions of schema](https://github.com/sankalpsrv/Schematise/blob/main/Notebook-of-approaches/Metamodel-RAG.ipynb)that can be used for tweaking LegalRuleML generated earlier.
- [Opened a dev branch](https://github.com/sankalpsrv/Schematise/tree/dev) - contains work on putting together the developed components. So far have uploaded the Azure Machine Learning Endpoints approach, will be adding more with local deployment.
- Tested various models and their quantisations for context windows, GPTQ quantised version accepts a larger context and the output is [uploaded in a notebook](https://github.com/sankalpsrv/Schematise/blob/main/Notebook-of-approaches/LocalLlama-LangChain.ipynb)

<img src = "./Flowchart.png" alt="A flowchart showing the different components of the programm which flows from Templates through to Part 1 where a combined XML is generated, and Part 2 where it is validated">

### Ethical considerations

- App shall provide a disclaimer before executing and at the generated results in each case regarding the results not constituting legal advice.
- No user data will be sought or stored in any place. The database integration will store the inference results for each statute.

### Resource constraints
I am working on a Cloud GPU when testing "local inferencing" via Llama2, and I am attempting to work with quantised models at this stage. However, OpenAI seems to provide a much more feasible deployment scenario. I will expand on capacities later, if required and for fine-tuning, such as by availing Azure. 

For the purposes of **app showcase** I intend on deploying via Cloud GPU, to the extent possible. Alternatively, will run on OpenAI as it is already integrated in the LangChain workflow. 


### LLMs being compared
HuggingFace's Transformers library will be made use of, in addition to Azure or any other comparable compute resources provider.

- Llama (useful because of its Grammars implementation)
 I have been able to generate similar output from Llama's 13b and 7b models via few-shot prompting. 
- GPT
I am using GPT3.5 for some idea testing and it has been delivering results consistently so far. I have shared these in my [notebook on the GitHub repository](www.github.com/sankalpsrv/Schematise/blob/main/Notebook-of-approaches/LangChain_FewShot.ipynb)

The following models will be considered later, if required
- Mixtral 7b instruct fine tuned
- BERT models
  - LegalBert (However, [this paper](https://www.sciencedirect.com/science/article/abs/pii/S0267364923000742) suggests that auto-encoding models perform lesser than autoregressive ones on this task)
  - InLegalBert (shown to perform better on Indian laws)


# TO-DOs

[Successful] Make a draft version of the app for review at the Hackday which will work on a representative set and generate compliances in Markdown/Text format.

[Unsuccessful] Find a teammember before 15th.

[Ongoing] Need to make a way to parse the templates that could be uploaded by the user.

[Ongoing] Update project page on hasgeek continuously. 

[Successful] Identify the correct chunking strategy for RAG. Share approaches as notebook.

[Ongoing] Use XML tools to validate and parse the XML generated by the LLM. 

[Ongoing] Test different LLMs described in the section above for their accuracy. Share results in separate folder as Jupyter Notebooks.

[Ongoing] Combine the different components into Part 1 - combined XML generation without validation

[] Combine the different components into Part 2 - XML validation and metamodel alignment

[] Create a modular set of classes to handle different options - Local and OpenAI

[] Upload the models as fine-tuned models once satisfactory performance is achieved.

[] Identify a way to benchmark or validate the performance of an LLM.

[] Draft a disclaimer for the app to show users.

[] Select copyright license.


# Roadmap

1. Develop a script that can take laws in text or PDF format and divide them by sections. 
  - This can include LLM based text-classification, however (see next point)
  - For a few standardised formats, this script should be able to do it without reliance on an LLM.
    - Need to explore to what extent an ANTLR serialisation can be developed for a few standard templates, and also whether it needs to be more dynamic than that.   
2. Implementing different LLM based text-generation approaches (list is indicative)
  - In-context learning for prompts that generate the LegalRuleML schema. This has already shown some results - [click here to see notebook that generated XML via prompt engineering](https://github.com/sankalpsrv/Schematise/blob/main/Notebook-of-approaches/Llama_Documentation_Prompting.ipynb)
  - Implement an approach that uses RAG, by processing the documentation provided for LegalRuleML. Currently looking at a way to implement 
  - LoRA adaptation using either HuggingFace, [Axolotl](https://github.com/OpenAccess-AI-Collective/axolotl) or Lit-GPT as outlined [here](https://cameronrwolfe.substack.com/p/easily-train-a-specialized-llm-peft).
  - Also will perform the training of a fine-tuned model on a custom-generated dataset, generated via an LLM model that allows for using its output for training (for e.g., OpenAI does not).
     - will use the dataset provided by Nyaaya-In as a way to fine-tune Llama2-7b-chat. Since this is provided under a Creative Commons ShareAlike license, I will create a separate branch for this approach. 
     - Alternatively, since In context learning has already shown some results, this will be used to create a fine-tuning dataset for some Environmental Laws (owing to the extensive compliance requirement there, which I have [previously researched on](https://sankalpsrv.in/2021/08/15/dissertation/).

3. **For fine tuning**:- Upload the models to huggingface and run validation tests for it on a repeated basis in order to identify whether further fine-tuning is required and to what extent.
   **For prompt engineering and fine-tuning approaches** - incorporate a way to verify the XML generated by the model, as also perform other XML level functions such as compacting and normalisation, ultimately for comparison.

4. Compare each of the approaches and select a default approach, as well as integrate each approach into the application.

5. Lastly, to save inference time, integrations with PostgreSQL/sqlite for the cached versions of laws will be stored in the working directory itself.
