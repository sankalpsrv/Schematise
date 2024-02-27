import langchain
from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from typing import List, Optional
from pydantic import Field
import model
import json
global_metamodels_to_process = [1, 2, 3, 4, 5, 6, 7]

metamodel_filename_dict = {
    "1": "context",
    "2": "defeasible",
    "3": "deontic",
    "4": "legaltemporal",
    "5": "metadata-actor",
    "6": "metadata-jurisdiction-authority",
    "7": "statement"
}

'''
class CustomRetriever(BaseRetriever):
    def __init__(self, metamodel_XML, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metamodel_XML = metamodel_XML

    def _get_relevant_documents(
            self, query: str = None, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        if query is None:
            query = self.metamodel_XML

        page_content = query
        return [Document(page_content=page_content)]
'''

def get_relevant_documents():
    
class CustomRetriever(BaseRetriever):
    page_content: Optional[str] = Field(default=None)

    def __init__(self, **data):
        super().__init__(**data)
        # Read file content and assign it to page_content field
        with open("Docs/metamodels_combined.txt", "r") as fn:
            self.page_content = fn.read()

    def _get_relevant_documents(
            self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> Optional[str]:
        # Directly use self.page_content, which is guaranteed to be present
        return self.page_content
def getRAG_metamodels(text_value, metamodel_number):
    metamodel_definitionfilename = str("Docs/" + metamodel_filename_dict[metamodel_number] + ".txt")
    metamodel_XMLfilename = str("Docs/" + metamodel_filename_dict[metamodel_number] + ".rdf")
    with open(metamodel_definitionfilename, 'r') as metamodel_definition_file:
        metamodel_definition = metamodel_definition_file.read()
    with open(metamodel_XMLfilename, 'r') as metamodel_XML_file:
        metamodel_XML = metamodel_XML_file.read()
    retrieverObj = CustomRetriever(metamodel_XML)
    metamodel_text_value = model.RAGPrompt(metamodel_XML, text_value, metamodel_definition)

    return metamodel_text_value
def similarity_tweaking(text_value, metamodels_to_process=global_metamodels_to_process):
    for metamodel_number in metamodels_to_process:
        metamodel_number = metamodel_number.strip()
        if metamodel_number != '':
            metamodel_text_value = getRAG_metamodels(text_value, metamodel_number)
            text_value = metamodel_text_value

    new_text_value = text_value


    return new_text_value



if __name__ == "__main__":



    value_of_key = data[0]['context']

    print(value_of_key)
