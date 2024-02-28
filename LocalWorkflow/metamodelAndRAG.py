import langchain
from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from typing import List, Optional
from pydantic import Field
import model
import json

import utils

global_metamodels_to_process = ["1", "2", "3", "4", "5", "6", "7"]

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
        return self.page_content
        #List[Document]:
        #return [Document(page_content=self.page_content)]
        # Directly use self.page_content, which is guaranteed to be present

def getRAG_metamodels(text_value, metamodel_number):
    metamodel = metamodel_filename_dict[metamodel_number]
    RetrieverObj = CustomRetriever()

    metamodel_text_value = model.RAGPrompt(RetrieverObj, text_value, metamodel, metamodel_number)

    return metamodel_text_value
def metamodel_operations(text_value, i, metamodels_to_process=global_metamodels_to_process):
    new_text_value = ''
    for metamodel_number in metamodels_to_process:
        metamodel_number = metamodel_number.strip()
        if metamodel_number != '':
            metamodel_text_value = getRAG_metamodels(text_value, metamodel_number)
            text_value = metamodel_text_value['text']
            filename = "Docs/" + "metamodel" + metamodel_number + "_" + str(i) + ".txt"
            with open(filename, "w") as fn:
                fn.write(text_value)

        new_text_value += utils.strip_code_block(str(text_value))


    return new_text_value



if __name__ == "__main__":
    ## This part for debugging only

    with open("_cache/text_value_stripped_2.txt", "r") as fn:
        text_value = fn.read()

    metamodel = getRAG_metamodels(text_value, metamodel_number = "1")

    toclean = metamodel['text']

    cleaned = utils.strip_code_block(toclean)

    print(cleaned)
    '''
    retrieverObj = CustomRetriever()

    retriever = retrieverObj.get_relevant_documents("The quick brown fox jumps over the")

    retriever = retriever.replace ('\n', '')
    retriever = retriever.replace ('\t', '')

    extra_data_index = 32969
    print(retriever[extra_data_index - 10: extra_data_index + 10])


    data = json.loads(retriever)

    value_of_key = data[1]['defeasible']

    print(value_of_key)
    '''

    '''
    prompt_template = """
        ### [INST] 
        <<SYS>> You are an assistant that takes the XML generated and tweaks it in accordance with the rdfs metamodel provided to you below as context. 
        The XML is in compliance with the LegalRuleML core specification, whereas the metamodel provides an overview of what the XML should be for a particular category of XML elements.
        The category being implemented is defined as follows:


        <</SYS>>
        Use the following metamodel to ensure that the XML generated is in terms of the definition of {metamodel} provided in the LegalRuleML specification.

        {metamodel_XML}

        ### QUESTION:
        {question} 

        [/INST]
        """

    rag_chain = (
            {"metamodel_XML": retrieverObj, "question": "Why is the sky blue?",
             "metamodel": "Testing"}
            | prompt_template
    )
    '''
    #print(reg_chain)