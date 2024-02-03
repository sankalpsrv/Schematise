from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import OpenAI
import pandas as pd
import csv
from secret_key import openai_key

import IK_interface

llm = OpenAI(openai_api_key=openai_key)



examples = [
    {
        "question": "Statute: Punishment for piracy - Whoever commits any act of piracy shall be punished with imprisonment for life or with fine or with both; or with death if the act of piracy causes death.",
        "answer": """
<LegalRuleML xmlns="http://www.oasis-open.org/committees/legalruleml">
  <lrml:PrescriptiveStatement id="PunishmentForPiracy">
    <lrml:Rule id="RuleForPiracyPunishment">
      <lrml:if>
      <lrml:Fact>
          <lrml:Rel iri="#commitPiracy"/>
        </lrml:Fact>
      </lrml:if>
      <lrml:then>
        <lrml:Obligation>
          <lrml:Sanction>
            <lrml:Penalty>
              <lrml:Type iri="#imprisonment"/>
              <lrml:Duration max="life"/>
            </lrml:Penalty>
            <lrml:Condition>
              <lrml:CausesDeathOrAttempt/>
              <lrml:AdditionalSanctions>
                <lrml:Restitution/>
                <lrml:ForfeitureOfProperty/>
              </lrml:AdditionalSanctions>
            </lrml:Condition>
          </lrml:Sanction>
        </lrml:Obligation>
      </lrml:then>
    </lrml:Rule>
  </lrml:PrescriptiveStatement>
</LegalRuleML>"""}]

example_prompt = PromptTemplate(
    input_variables=["question", "answer"], template="Question: {question}\n{answer}"
)

prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    suffix="Question: {input}",
    input_variables=["input"],
)

def law_parser(doc_number, df_condition):

    IK_interface.extract_text(doc_number)
    csv_filename = 'sections.csv' # file containing all the sections from the E-Waste Rules, generated via IK_interface function


    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(csv_filename)

    if df_condition == "1":
        df2 = df.head(10)
    else:
        df2=df.copy()

    # Now, 'df' contains the data from the CSV file
    # You can perform various operations on the DataFrame
    combined_response = ''
    # Iterate through rows and process the data
    for index, row in df2.iterrows():
        section_title = row['Section Title']
        nested_content = row['Nested Content']

        # Process section_title and nested_content as needed
        #print(f"Section Title: {section_title}")
        #print(f"Nested Content: {nested_content}\n")
        combined_text = f"{section_title}: {nested_content}\n"

        prompt_for_input=prompt.format(input=combined_text)

        #print ("Input prompt is", prompt_for_input)

        response=llm.invoke(prompt_for_input)

        #print ("Response is", response)

        combined_response += response

    return combined_response
        




