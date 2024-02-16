# Schematise (formerly "Complianalyse")
### Submission to [The Fifth Elephant's Open Source AI Hackathon](https://hasgeek.com/fifthelephant/open-source-ai-hackathon/)
An LLM enabled schema generator for statutes in the Akoma Ntoso format. 

# How to run (proof of concept version)

### Requirements

- OpenAI Key (make an account on openai.com and get keys https://platform.openai.com/api-keys)
- IndianKanoon API Key (sign up and obtain key via https://api.indiankanoon.org)

1. Install python.
2. (Optional) Create virtual environment - `virtualenv complianalyse`
   `source /complianalyse/bin/activate` 
3. Install requirements via txt file `pip install -r requirements.txt`
4. run `python main.py` and follow steps
   
# Roadmap

1. Develop a script that can take laws in text or PDF format and divide them by sections.
  - This can include LLM based text-classification, however (see next point)
  - For a few standardised formats, this script should be able to do it without reliance on an LLM.
    - Need to explore to what extent an ANTLR serialisation can be developed for a few standard templates, and also whether it needs to be more dynamic than that.   
2. Implementing different LLM based text-generation approaches (list is indicative at this point)
  - In-context learning for prompts that generate the LegalRuleML schema. This has already shown some results. [Link to ChatGPT prompts that generated results (will replicate further with programmatic access)](https://chat.openai.com/share/04a01b6f-7829-4765-84f8-9038e9d68666)
  - Implement an approach that uses RAG, by processing the documentation provided for LegalRuleML. 
  - LoRA adaptation using either HuggingFace, [Axolotl](https://github.com/OpenAccess-AI-Collective/axolotl) or Lit-GPT as outlined [here](https://cameronrwolfe.substack.com/p/easily-train-a-specialized-llm-peft).
  - Also will perform the training of a fine-tuned model on a custom-generated dataset, generated via an LLM model that allows for using its output for training (for e.g., OpenAI does not). Since In context learning has already shown some results, this will be used to create a fine-tuning dataset for some Environmental Laws (owing to the extensive compliance requirement there, which I have [previously researched on](https://sankalpsrv.in/2021/08/15/dissertation/).

3. Upload the models to huggingface and run validation tests for it on a repeated basis in order to identify whether further fine-tuning is required and to what extent.

4. Compare each of the approaches and select a default approach, as well as integrate each approach into the application.

5. Lastly, to save inference time, integrations with PostgreSQL/sqlite for the cached versions of laws will be stored in the working directory itself.

# TO-DOs

[x] Make a draft version of the app for review at the Hackday which will work on a representative set and generate compliances in Markdown/Text format.

[-] Find a teammember before 15th.

[] Need to make a way to parse the templates that could be uploaded by the user.

[x] Update project page on hasgeek continuously. 

[] Identify the correct chunking strategy for RAG. Share approaches as notebook.

[x] Test different LLMs described in the section above for their accuracy. Share results in separate folder as Jupyter Notebooks.

[] Upload the models as fine-tuned models once satisfactory performance is achieved.

[] Identify a way to benchmark or validate the performance of an LLM.

[] Draft a disclaimer for the app to show users.

[] Select copyright license.

# Progress

- Was able to test the few-shot learning in-context learning approach via LangChain and OpenAI. Due to token limits on LangChain, using a split approach was necessary.
- Nevertheless, was able to generate LegalRuleML code via this approach - [available in this notebook (click here)](https://github.com/sankalpsrv/Complianalyse/blob/main/LangChain_FewShot.ipynb)
- The test output generated for the entire Bio-medical Waste Rules is here - [testbmw.txt](https://github.com/sankalpsrv/Complianalyse/blob/main/src/testbmw.txt)
- This was generated using the script in the ["src" folder of this repository (click here)](https://github.com/sankalpsrv/Complianalyse/blob/main/src/main.py)
- Tested Llama through LangChain and AzureML Endpoints, found that it works via Azure, while LangChain presents some difficulties [click here to view notebook](https://github.com/sankalpsrv/Schematise/blob/main/Notebook-of-approaches/Llama2_AzureMl_CompletionsAPIAndChatAPI(1).ipynb)
