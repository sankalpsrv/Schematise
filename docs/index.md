# Welcome to the Schematise Documentation

CLICK HERE TO ACCESS [THE HOSTED STREAMLIT APP](https://schematise.streamlit.app)

CLICK HERE TO ACCESS [THE GITHUB REPO](https://github.com/sankalpsrv/Schematise)

- Developed by Sankalp Srivastava for the FifthElephant's Open Source AI Hackathon.

- It is a statute to XML converter that seeks maximum possible adherence with the AkomaNtoso and LegalRuleML family of XML formats.

- This documentation site was created to guide further development and may be incomplete. For further queries, reach out to the creator through one of the profiles linked [here](https://sankalpsrv.in)

## Project layout (documentation)

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        Schematise_py-and-main_py.md       
        model_py.md
        combinedprocess_py.md
        metamodelAndRAG_py.md
        utils_py.md


### How to use the Streamlit app:

##### Main-page:

1. Choose whether you want to upload the CSV file or proceed with an IndianKanoon URL.
2. If selected “Upload”, put a CSV file in the format provided on the link in the app. For reference, see point number 2 of requirements. You can also leave blank to work with the default CSV, which is the E-Waste (Management) Rules, 2016.
3. Choose LegalDocML or LegalRuleML as the format you want the XML in. Only one is generated at a time. Metamodel can be applied for tweaking only if LegalRuleML is selected.
4. Enter the starting range and ending range as the rows you want the XML generated for, from the CSV.
5. Check the checkbox for viewing the dataframe to preview the rows you have selected from the CSV.
6. Choose OpenAI as the LLM. Llama2 support for the UI app is yet to come.
7. Click “Download XML generated” to get the XML generated in the format you have chosen as a “.txt” file. 

##### Metamodel page:

1. Choose which metamodel you would like to provide as context to the LLM to modify the LegalRuleML generated in accordance with. These are 7 of the metamodels chosen from the LegalRuleML core specification page. 
    1. Context
    2. Defeasible
    3. Deontic
    4. Legal Temporal
    5. Metadata actor
    6. Metadata jurisdiction authority
    7. Statement
2. After choosing, the metamodel is automatically generated.
3. Click “Download XML generated” to get the XML generated in the format you have chosen as a “.txt” file.
4. You can choose to opt for more tweaking, by choosing the option described in step 1 again. 

##### Similarity page:

1. Select two index numbers (starts with zero) that you want to check for similarities.
2. If both the XML fragments are well-formed, it will immediately present the similarities between the different XML element tags and attributes.
3. If either XML fragment does not validate, then you will be provided the XML fragment along with the option to either upload or edit the XML. 
4. After editing, or uploading the XML fragment, you can download the edited XML. 

### FAQ:

1. Why “.txt” format for downloading the XML? 
   This format is chosen because the XML generated will have to be well formed and validated before it is stored as a “.xml” file. See “Similarity page” for more details. 
2. Why do I need to provide an IndianKanoon key?
   It is not necessary to provide an IndianKanoon key, you can proceed with an uploaded csv file in the format available at the [following link (click here to view)](https://raw.githubusercontent.com/sankalpsrv/Schematise/dev/fullsections.csv).
3. Why do I have to provide my OpenAI key?
   The Streamlit community cloud hosted version works with OpenAI. However, you can always use the local inferencing available on the [GitHub repository (click here to visit)](https://github.com/sankalpsrv/Schematise)
4. Why can metamodel only be used for “LegalRuleML”?
   This is because of the availability of a metamodel for LegalRuleML, which is not the case for LegalDocML. However, in the future version, identifiable aspects of the LegalDocML documentation with examples will also be added.
5. Why are only 7 of the metamodels used as context?
   The metamodels to be provided as context were chosen on the basis of their coverage of the concepts defined in the LegalRuleML core specification. You can view the paragraphs chosen as context in the file [“metamodels_combined” in the “Docs” folder](https://github.com/sankalpsrv/Schematise/blob/dev/Streamlit/Docs/metamodels_combined.txt) 
   The following metamodels were excluded:
   - “Alternative” – seeks to implement alternative interpretations, which does not occur as the LLM is not prompted for it;
   - “Rulemm” – contains distinct elements which appear to be mutually exclusive and without documentation in the LegalRuleML core specification;
   - “Source” – contains the elements for describing where the text has been ‘sourced’ from, which will require a specific input by the user;
   - “Upper” – contains the elements associated with comments passed, which is not something that the LLM is being prompted for.
   - “Wrapper” – contains enclosing XML elements only for various purposes and they do not pertain to a single  category of elements.
6. What is the similarity page for?
   It has been noticed that the XML which is generated through successive iteration through the CSV files can have an inconsistent representation of provisions in XML elements or attributes. In other words, similarly named elements and attributes are generated where an element or attribute should have had the same name as was for an earlier generated XML for a section. This page allows you to detect this similarity using Python’s [“TheFuzz” library’s Simple Ratio](https://pypi.org/project/thefuzz/). 

        
        