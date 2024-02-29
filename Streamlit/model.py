import requests
import os
import urllib.request
import ssl
import json

from langchain_core.output_parsers import StrOutputParser
output_parser = StrOutputParser()

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


from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_openai import ChatOpenAI

import torch, gc
hf_global = HuggingFacePipeline()
llm_global = "openaiselected"
openai_key = os.getenv('OPENAI_API_KEY')
openai_chain = ChatOpenAI(openai_api_key=openai_key)

# https://discuss.pytorch.org/t/how-can-we-release-gpu-memory-cache/14530/27
def clear_torch_cache():
    '''def _optimizer_to(device):
        for param in self.optimizer.state.values():
            # Not sure there are any global tensors in the state dict
            if isinstance(param, torch.Tensor):
                param.data = param.data.to(device)
                if param._grad is not None:
                    param._grad.data = param._grad.data.to(device)
            elif isinstance(param, dict):
                for subparam in param.values():
                    if isinstance(subparam, torch.Tensor):
                        subparam.data = subparam.data.to(device)
                        if subparam._grad is not None:
                            subparam._grad.data = subparam._grad.data.to(device)
    _optimizer_to(torch.device('cpu'))
    '''
    gc.collect()
    torch.cuda.empty_cache()



def instantiate_model(llm="openaiselected"):
    global llm_global
    llm_global = llm
    if llm != 'openaiselected':

        ## THIS PART IS COMMENTED OUT ON LOCAL CPU DEPLOYMENT

        model_name_or_path = "TheBloke/Llama-2-7B-Chat-GPTQ"
        # To use a different branch, change revision
        # For example: revision="main"
        model = AutoModelForCausalLM.from_pretrained(model_name_or_path,
                                                     device_map="auto",
                                                     trust_remote_code=True,
                                                     revision="main")

        tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)

        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_length=4000,
            do_sample=True,
            temperature=0.7,
            top_p=0.95,
            top_k=40,
            repetition_penalty=1.1
        )
        global hf_global
        hf = HuggingFacePipeline(pipeline=pipe)
        hf_global = hf


    # noinspection PyUnreachableCode
def send_request(section_for_conversion, llm):
    instantiate_model(llm)
    global llm_global
    global hf_global
    hf = hf_global
    examples = [
        {
            "question": "Convert this statute extract to Legal Rule ML XML format: The benefit referred to in comma 1 shall be paid in an amount equal 80 per cent of five-twelfths of the income earned and reported for tax purposes by the freelancer in the second year preceding the year of application.",
            "answer": """<lrml:ConstitutiveStatement key="tax2">

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

</lrml:PrescriptiveStatement>"""
        },
        {
            "question": "Convert this statute extract to Legal Rule ML XML format:A person must not engage in a credit activity if the person does not hold a licence authorising the person to engage in the credit activity. Civil penalty: 2,000 penalty units.  Criminal penalty: 200 penalty units, or 2 years imprisonment, or both.",
            "answer": """
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
        }
    ]
    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{question}"),
            ("ai", "{answer}"),
        ]

    )

    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
    )

    final_prompt = ChatPromptTemplate.from_messages(
        [
            ("system",
             "You are a consistent Legal Rule ML converter who takes the statute text as input and outputs the XML format for the same with reference to the documentation available at http://docs.oasis-open.org/legalruleml/legalruleml-core-spec/v1.0/legalruleml-core-spec-v1.0.html"),
            few_shot_prompt,
            ("human", "{question}"),
        ]
    )
    if llm_global == "openaiselected":
        llm_chain = final_prompt | openai_chain | output_parser
    else:
        llm_chain = final_prompt | hf

    result = llm_chain.invoke({"question": section_for_conversion})

    return result

def RAGPrompt (RetrieverObj, text_value, metamodel, metamodel_number):
    global global_metamodel
    global_metamodel= metamodel
    global global_metamodel_number
    global_metamodel_number = metamodel_number
    instantiate_model()
    global hf_global
    hf = hf_global

    # Since the context window did not have system_prompt, it was returning a deficient output (asking for more information or context)
    # In this strategy, the human_prompt itself is being used to provide the system prompt as context, using the tags accepted by Llama2 (see https://huggingface.co/blog/llama2)
    sys_prompt = """ou are an assistant that takes the XML generated and tweaks it in accordance with the rdfs metamodel provided to you below as context. 
        The XML is in compliance with the LegalRuleML core specification, whereas the metamodel provides an overview of what the XML should be for a particular category of XML elements."""
    human_prompt = """
        ### [INST] 
            <<SYS>>
            {system_prompt}

            The category being implemented is defined as follows:

            {metamodel_definition}

             <</SYS>>
            Use the following metamodel in RDFS to ensure that the XML generated is in terms of the definition of the metamodel provided in the LegalRuleML specification.

            {metamodel_XML}


            ### LEGAL_XML:
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

    template = ChatPromptTemplate.from_messages([
        ("system", sys_prompt),
        ("human", human_prompt)
    ])


    llm_chain = LLMChain(llm=hf, prompt=template)

    input_dict = {
        "system_prompt": sys_prompt,
        "metamodel_definition": RetrieverObj|get_relevant_definition,
        "metamodel_XML": RetrieverObj|get_relevant_metamodel,
        "question": text_value,
    }

    new_text_value = llm_chain.invoke(input=input_dict)

    return new_text_value
