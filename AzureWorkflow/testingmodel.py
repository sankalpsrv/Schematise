import requests
import os
import urllib.request
import ssl
import json

from langchain.schema import HumanMessage
from langchain_community.llms.azureml_endpoint import AzureMLEndpointApiType
from langchain_community.chat_models.azureml_endpoint import AzureMLChatOnlineEndpoint
from langchain_community.chat_models.azureml_endpoint import LlamaChatContentFormatter

from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.few_shot import FewShotChatMessagePromptTemplate
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

import metamodelAndRAG
from metamodelAndRAG import CustomRetriever

llm = AzureMLChatOnlineEndpoint(
    endpoint_url="",
    endpoint_api_type=AzureMLEndpointApiType.serverless,
    endpoint_api_key="",
    content_formatter=LlamaChatContentFormatter(),
    model_kwargs={"temperature": 0.4, "max_tokens": 2000}
)

prompt_template = """
    ### [INST] 
    <<SYS>> You are an assistant that takes the XML generated and tweaks it in accordance with the rdfs metamodel provided to you below as context. 
    The XML is in compliance with the LegalRuleML core specification, whereas the metamodel provides an overview of what the XML should be for a particular category of XML elements.
    The category being implemented is defined as follows:

    {metamodel_definition}

    <</SYS>>
    Use the following metamodel to ensure that the XML generated is in terms of the definition of the metamodel provided in the LegalRuleML specification.

    {metamodel_XML}

    ### QUESTION:
    {question} 

    [/INST]
    """


# Use the following values as placeholders
def get_relevant_metamodel(RetrieverObj):

    docs = RetrieverObj.get_relevant_documents("query")

    docs = docs.replace('\n', '')
    docs = docs.replace('\t', '')

    data = json.loads(docs)

    relevant_metamodel = data[2]["deontic"]
    return relevant_metamodel


def get_relevant_definition(RetrieverObj):
    docs = RetrieverObj.get_relevant_documents("query")
    docs = docs.replace('\n', '')
    docs = docs.replace('\t', '')

    data = json.loads(docs)

    relevant_definition = data[2]["description"]
    return relevant_definition


# Abstraction of Prompt
prompt = ChatPromptTemplate.from_template(prompt_template)
output_parser = StrOutputParser()
RetrieverObj = CustomRetriever()
# Creating an LLM Chain
llm_chain = LLMChain(llm=llm, prompt=prompt)

text_value = """
<lrml:LegalSources>
  <lrml:LegalSource key="ls1" sameAs="http://www.centralpollutioncontrolboard.gov.in/">
    <lrml:appliesAssociations>
      <lrml:Associations>
        <lrml:Association keyref="#ps1"/>
      </lrml:Associations>
    </lrml:appliesAssociations>
  </lrml:LegalSource>
</lrml:LegalSources>

<lrml:Context key="psInfo1">
  <lrml:appliesAssociations>
    <lrml:Associations>
      <lrml:Association keyref="#ps1"/>
    </lrml:Associations>
  </lrml:appliesAssociations>
</lrml:Context>

<lrml:PrescriptiveStatement key="ps1">
  <ruleml:Rule key=":rule1" closure="universal">
    <lrml:hasStrength>
      <lrml:DefeasibleStrength key="str1" iri="&defeasible-ontology;#defeasible1"/>
    </lrml:hasStrength>
    <ruleml:if>
      <ruleml:Atom>
        <ruleml:Rel iri=":facilities"/>
        <ruleml:Var>X</ruleml:Var>
      </ruleml:Atom>
    </ruleml:if>
    <ruleml:then>
      <lrml:SuborderList>
        <lrml:Prohibition>
          <ruleml:Atom>
            <ruleml:Rel iri=":notInAccordanceWithStandards"/>
            <ruleml:Var>X</ruleml:Var>
          </ruleml:Atom>
        </lrml:Prohibition>
      </lrml:SuborderList>
    </ruleml:then>
  </ruleml:Rule>
</lrml:PrescriptiveStatement>
"""
# RAG Chain
rag_chain = {
    "metamodel_XML": get_relevant_metamodel(RetrieverObj),
    "metamodel_definition": get_relevant_definition(RetrieverObj),
    "question": text_value
}
print(llm_chain(rag_chain))