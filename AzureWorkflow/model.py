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


def send_request(section_for_conversion):
    data = {
        "messages": [
            {
                "role": "system",
                "content": "You are a consistent Legal Rule ML converter who takes the statute text as input and outputs the XML format for the same with reference to the documentation available at http://docs.oasis-open.org/legalruleml/legalruleml-core-spec/v1.0/legalruleml-core-spec-v1.0.html"
            },
            {
                "role": "user",
                "content": "Convert this statute extract to Legal Rule ML XML format: The benefit referred to in comma 1 shall be paid in an amount equal 80 per cent of five-twelfths of the income earned and reported for tax purposes by the freelancer in the second year preceding the year of application."
            },
            {
                "role": "assistant",
                "content": """
          <lrml:ConstitutiveStatement key="tax2">

          <ruleml:Rule closure="universal">

        <lrml:Paraphrase>If income is reported in some year, then it was earned in the previous year.

        </lrml:Paraphrase>

        <ruleml:if>

          <ruleml:Atom>

            <ruleml:Rel iri=":reported"/>

            <ruleml:Var>income</ruleml:Var>

            <ruleml:Var>year</ruleml:Var>

          </ruleml:Atom>

        </ruleml:if>

        <ruleml:then>

          <ruleml:Atom>

            <ruleml:Rel iri=":earned"/>

            <ruleml:Var>income</ruleml:Var>

            <ruleml:Expr key=":year-1">

              <ruleml:Fun iri=":subtract"/>

              <ruleml:Var>year</ruleml:Var>

              <ruleml:Data xsi:type="xs:integer">1</ruleml:Data>

            </ruleml:Expr>

          </ruleml:Atom>

        </ruleml:then>

      </ruleml:Rule>

    </lrml:ConstitutiveStatement>
    <lrml:PrescriptiveStatement key="literal">

    <ruleml:Rule closure="universal" key=":literal-template">

        <ruleml:if>

            <ruleml:And>

                <ruleml:Atom key=":atom-earned">

                    <ruleml:Rel iri=":earned"/>

                     <ruleml:Var>income</ruleml:Var>

                     <ruleml:Expr>

                        <ruleml:Fun iri=":subtract"/>

                        <ruleml:Var>year</ruleml:Var>

                        <ruleml:Data xsi:type="xs:integer">2</ruleml:Data>

                     </ruleml:Expr>

                 </ruleml:Atom>

                 <ruleml:Atom key=":atom-reported">

                     <ruleml:Rel iri=":reported"/>

                     <ruleml:Var>income</ruleml:Var>

                    <ruleml:Expr>

                         <ruleml:Fun iri=":subtract"/>

                         <ruleml:Var>year</ruleml:Var>

                         <ruleml:Data xsi:type="xs:integer">2</ruleml:Data>

                     </ruleml:Expr>

                 </ruleml:Atom>

            </ruleml:And>

        </ruleml:if>

        <ruleml:then>

             <lrml:Obligation key="obl-paybenefit">

                  <ruleml:slot>

                      <lrml:Bearer/>

                      <ruleml:Var>Employer</ruleml:Var>

                  </ruleml:slot>

                  <ruleml:slot>

                      <lrml:AuxiliaryParty/>

                      <ruleml:Var>Freelancer</ruleml:Var>

                  </ruleml:slot>

                  <ruleml:Atom>

                      <ruleml:Rel iri=":paybenefit"/>

                     <ruleml:Expr>

                          <ruleml:Fun iri=":80_percent_of_five-twelfths_of"/>

                          <ruleml:Var>income</ruleml:Var>

                      </ruleml:Expr>

                      <ruleml:Var>year</ruleml:Var>

                  </ruleml:Atom>

              </lrml:Obligation>

          </ruleml:then>

      </ruleml:Rule>

</lrml:PrescriptiveStatement>
    """
            },
            {
                "role": "user",
                "content": "Convert this statute extract to Legal Rule ML XML format:A person must not engage in a credit activity if the person does not hold a licence authorising the person to engage in the credit activity. Civil penalty: 2,000 penalty units.  Criminal penalty: 200 penalty units, or 2 years imprisonment, or both."
            },
            {
                "role": "assistant",
                "content": """

<lrml:LegalSources>

   <lrml:LegalSource key="ls1"             sameAs="http://www.comlaw.gov.au/Details/C2009A00134/Html/Text#param43"/>

</lrml:LegalSources>


<lrml:Context key="psInfo1">

   <lrml:appliesAssociations>

          <lrml:Associations>

                <lrml:Association>

                       <lrml:appliesSource keyref="#ls1/>

                       <lrml:toTarget keyref="#ps1"/>

                       <lrml:toTarget keyref="#ps2"/>

                       <lrml:toTarget keyref="#pen1"/>

                       <lrml:toTarget keyref="#pen2"/>

                </lrml:Association>

          </lrml:Associations>

</lrml:appliesAssociations>

</lrml:Context>


<lrml:Statements key="textblock1">

<lrml:hasQualification>

  <lrml:Override over="#ps2" under="#ps1"/>

  </lrml:hasQualification>

  <lrml:PrescriptiveStatement key="ps1">

      <ruleml:Rule key=":rule1" closure="universal">

        <lrml:hasStrength>

          <lrml:DefeasibleStrength key="str1" iri="&defeasible-ontology;#defeasible1"/>

        </lrml:hasStrength>

        <ruleml:if>

          <ruleml:Atom>

            <ruleml:Rel iri=":person"/>

            <ruleml:Var>X</ruleml:Var>

          </ruleml:Atom>

        </ruleml:if>

        <ruleml:then>

          <lrml:SuborderList>

            <lrml:Prohibition>

              <ruleml:Atom>

                <ruleml:Rel iri=":engageCreditActivity"/>

                <ruleml:Var>X</ruleml:Var>

              </ruleml:Atom>

            </lrml:Prohibition>

          </lrml:SuborderList>

        </ruleml:then>

      </ruleml:Rule>

    </lrml:PrescriptiveStatement>



    <lrml:PenaltyStatement key="pen2">

      <lrml:SuborderList>

        <lrml:Obligation>

          <ruleml:Atom>

            <ruleml:Rel iri=":payPenalUnits"/>

            <ruleml:Var>X</ruleml:Var>

            <ruleml:Ind>200</ruleml:Ind>

          </ruleml:Atom>

        </lrml:Obligation>

        <lrml:Obligation>

          <ruleml:Atom>

            <ruleml:Rel iri=":imprisonment"/>

            <ruleml:Var>X</ruleml:Var>

            <ruleml:Ind>2 years</ruleml:Ind>

          </ruleml:Atom>

        </lrml:Obligation>

        <lrml:Obligation>

          <ruleml:Atom>

            <ruleml:Rel iri=":payPenalUnitPlusImprisonment"/>

            <ruleml:Var>X</ruleml:Var>

            <ruleml:Ind>200</ruleml:Ind>

            <ruleml:Ind>2 years</ruleml:Ind>

          </ruleml:Atom>

        </lrml:Obligation>

      </lrml:SuborderList>

    </lrml:PenaltyStatement>



    <lrml:ReparationStatement key="rep1">

      <lrml:Reparation key="assoc1">

        <lrml:appliesPenalty keyref="#pen1"/>

        <lrml:toPrescriptiveStatement keyref="#ps1"/>

      </lrml:Reparation>

    </lrml:ReparationStatement>

    <lrml:ReparationStatement key="rep2">

      <lrml:Reparation keyref="#assoc1">

        <lrml:appliesPenalty keyref="#pen2"/>

        <lrml:toPrescriptiveStatement keyref="#ps1"/>

      </lrml:Reparation>

    </lrml:ReparationStatement>

</lrml:Statements>
"""
            },
            {
                "role": "user",
                "content": f"""Convert this extract of a statute to LegalRuleML XML format: {section_for_conversion}"""
            }
        ],
        "temperature": 0.25,
        "max_tokens": 4000
    }

    body = str.encode(json.dumps(data))

    url = ''
    # Replace this with the primary/secondary key or AMLToken for the endpoint
    api_key = ''
    if not api_key:
        raise Exception("A key should be provided to invoke the endpoint")

    headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()
        # print(result)

        return result

    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context


allowSelfSignedHttps(True)  # this line is needed if you use self-signed certificate in your scoring service.



# Request data goes here
# The example below assumes JSON formatting which may be updated
# depending on the format your endpoint expects.
# More information can be found here:
# https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
def RAGPrompt(retrieverObj, text_value, metamodel, metamodel_number):
    global global_metamodel
    global_metamodel= metamodel
    global global_metamodel_number
    global_metamodel_number = metamodel_number
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
    def get_relevant_metamodel(retrieverObj):
        docs = retrieverObj.get_relevant_documents("query")

        docs = docs.replace('\n', '')
        docs = docs.replace('\t', '')

        data = json.loads(docs)

        relevant_metamodel = data[2]["deontic"]
        return relevant_metamodel

    def get_relevant_definition(retrieverObj):
        docs = retrieverObj.get_relevant_documents("query")
        docs = docs.replace('\n', '')
        docs = docs.replace('\t', '')

        data = json.loads(docs)

        relevant_definition = data[2]["description"]
        return relevant_definition

    # Abstraction of Prompt
    prompt = ChatPromptTemplate.from_template(prompt_template)
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    rag_chain = {
        "metamodel_XML": get_relevant_metamodel(retrieverObj),
        "metamodel_definition": get_relevant_definition(retrieverObj),
        "question": text_value
    }

    new_text_value = llm_chain(rag_chain)

    return new_text_value
