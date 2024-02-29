# Important: This is in-development, only for internal use amongst mentors.

Features currently implemented:
1. XML generation by prompting every section with the context of a few-shot-template in Streamlit, Azure and Local Workflow.
2. Automatic metamodel alignment in Azure (automatically aligning with all 7 metamodels utilised in this program).
3. Manual metamodel alignment in Azure (by specifying which of the 7 metamodels and the order you want to align the XML with them in).

### How to run:

0. Run the following command or download the ZIP file for the "dev" branch - `git clone -b dev https://github.com/sankalpsrv/Schematise.git`

### For Streamlit App - Follow steps 1-6 here

1. Change directory to "Streamlit" and install the requirements (preferably in a conda shell) using - `pip install -r serverrequirements.txt` and `pip install streamlit`
   Also add conda environment packages using `conda env create -f condaenvironment.yml`
2. Download the sections you want and put them in the format of two columns representing "Section Title" and "Nested Content" with the latter containing all the nested contents inside the Section Title. For reference, see the E-waste rules parsed in this format, as "fullsections.csv"
3. Add open ai key to .env file using "OPENAI_API_KEY" as the key, alternatively enter it manually in line 31 of `model.py`.
4. Run the streamlit app by executing `streamlit run streamlit run streamlit-Schematise.py`
5. Browse and upload file created above in step 2.
6. Specify range of sections (for pandas dataframe) you want the XML for.
7. Select OpenAI or Llama2-7b-GPTQ as the model to use in the options.
8. Wait for XML to be generated for range of sections specified. You can view already done processing in the terminal or in the _cache folder for now.

### For Local Deployment - Follow steps 1-4 here

1. Change directory to "LocalWorkflow" and install the requirements (preferably in a conda shell) using - `pip install -r serverrequirements.txt`
   Also add conda environment packages using `conda env create -f condaenvironment.yml`
2. Download the sections you want and put them in the format of two columns representing "Section Title" and "Nested Content" with the latter containing all the nested contents inside the Section Title. For reference, see the E-waste rules parsed in this format, as "fullsections.csv"
3. Specify your model from HugingFace in Line 54 of model.py - I use GPTQ quantisation because of the larger context window.
4. Run `python main.py`

### For Azure Workflow - Follow steps 1-6 below

1. Change directory to "AzureWorkflow" and install the requirements (preferably in a virtual environment) using - `pip install -r requirements27th.txt`
2. Download the sections you want and put them in the format of two columns representing "Section Title" and "Nested Content" with the latter containing all the nested contents inside the Section Title. For reference, see the E-waste rules parsed in this format, as "fullsections.csv"
3. Specify the range of sections you want to run in utils.csv_parser (at line number 14) - defaulted to Sections 71-73
4. Put in your Azure endpoint URL and api_key for the Llama Chat 7b model at lines 369-371 and 415-417 of `model.py`
5. Run main.py with the argument --xmlh (for manual metamodel alignment) and --xmla (for automatic metamodel alignment)
6. Specify the interval at which you want the sections for which the XML is generated successively to be aligned when prompted for the same.

### Need to implement the entire program on a local machine, hence the current code will undergo changes 


### Goal for the workflow 

<img src = "./Flowchart.png">
