def strip_code_block(string):
    #Find the first occurrence of ```
    start_index = string.find('```')
    end_index = len(string)
    no_start_index = False
    no_end_index = False
    if start_index == -1:
        no_start_index = True # No code block found
        start_index = 0
    else:
        start_index += 3

    # Find the next occurrence of ``` after the first one
    end_index = string.find('```', start_index + 3)
    if end_index == -1:
        no_end_index = True
        end_index = len(string)# No closing code block found
    else:
        pass

    # Extract the part between the first and last ```
    extracted_string = string[start_index:end_index]



    #extracted_string = string
    # Find the index of the first occurrence of '<' after removing the code block
    index_of_first_opening_bracket = extracted_string.find('<')

    # Find the index of the last closing bracket
    index_of_last_closing_bracket = find_last_closing_tag_index(string)

    # Extract the part of the string between the first opening '<' and the last closing '>'
    if index_of_first_opening_bracket != -1 and index_of_last_closing_bracket != -1:
        result = extracted_string[index_of_first_opening_bracket -1:index_of_last_closing_bracket +1]
    elif index_of_first_opening_bracket != -1 and index_of_last_closing_bracket == -1:
        result = extracted_string[index_of_first_opening_bracket -1:]
    elif index_of_first_opening_bracket != -1 and index_of_last_closing_bracket != -1:
        result = extracted_string[:index_of_last_closing_bracket+1]
    else:
        result = extracted_string

    return result


import re


def find_last_closing_tag_index(xml_string):
    # Regular expression to match closing XML tags
    pattern = r'<\/.*>'

    # Find all occurrences of the closing tags
    matches = list(re.finditer(pattern, xml_string))

    # Check if there are any matches
    if matches:
        # Get the last match
        last_match = matches[-1]
        # Return the start index of the last closing tag
        return last_match.end()
    else:
        # Return an indication that no closing tag was found
        return -1
def remove_linebreaks(s):
    return s.replace("""\n""", " ")

def func(value):
    return ''.join(value.splitlines())


if __name__ == '__main__':
    statute_extract = """```\n\n<lrml:LegalSources>\n  <lrml:LegalSource key="ls1" sameAs="http://www.eco.gov.in/sites/default/files/pdf_file/E-Waste%20Rules%2C%202016.pdf"``` Note"""
    statute_extract = """
    Here is the statute extract in LegalRuleML XML format:
```
<lrml:LegalSources>
  <lrml:LegalSource key="ls1">
    <lrml:uri>http://www.example.com/statutes/e-waste.html</lrml:uri>
  </lrml:LegalSource>
</lrml:LegalSources>

<lrml:Context key="psInfo1">
  <lrml:appliesAssociations>
    <lrml:Associations>
      <lrml:Association keyref="#ps1">
        <lrml:appliesSource keyref="#ls1"/>
        <lrml:toTarget keyref="#rep1"/>
        <lrml:toTarget keyref="#rep2"/>
      </lrml:Association>
    </lrml:Associations>
  </lrml:appliesAssociations>
</lrml:Context>

<lrml:Statements key="textblock1">
  <lrml:hasQualification>
    <lrml:DefeasibleStrength key="str1" iri="http://defee.org/defeasible-ontology#defeasible1"/>
  </lrml:hasQualification>
  <lrml:PrescriptiveStatement key="ps1">
    <ruleml:Rule key=":rule1" closure="universal">
      <lrml:if>
        <lrml:Atom>
          <lrml:Rel iri=":collectEWaste"/>
          <lrml:Var>X</lrml:Var>
        </lrml:Atom>
      </lrml:if>
      <lrml:then>
        <lrml:SuborderList>
          <lrml:Prohibition>
            <ruleml:Atom>
              <lrml:Rel iri=":collectEWasteOnBehalfOfProducer"/>
              <lrml:Var>X</lrml:Var>
            </ruleml:Atom>
          </lrml:Prohibition>
          <lrml:Prohibition>
            <ruleml:Atom>
              <lrml:Rel iri=":collectEWasteOnBehalfOfDismantlerRefurbisherRecyclerOrphanedProducts"/>
              <lrml:Var>X</lrml:Var>
            </ruleml:Atom>
          </lrml:Prohibition>
        </lrml:SuborderList>
      </lrml:then>
    </ruleml:Rule>
  </lrml:PrescriptiveStatement>
</lrml:Statements>

<lrml:PenaltyStatement key="rep1">
  <lrml:Reparation key="assoc1">
    <lrml:appliesPenalty keyref="#pen1"/>
    <lrml:toPrescriptiveStatement keyref="#ps1"/>
  </lrml:Reparation>
</lrml:PenaltyStatement>

<lrml:PenaltyStatement key="rep2">
  <lrml:Reparation keyref="#assoc1">
    <lrml:appliesPenalty keyref="#pen2"/>
    <lrml:toPrescriptiveStatement keyref="#ps1"/>
  </lrml:Reparation>
</lrml:PenaltyStatement>
```
Explanation:

* `<lrml:LegalSources>` i    """
    stripped_statute_extract = strip_code_block(statute_extract)
    #print(stripped_statute_extract)



    with open ("./_cache/xml_file_test.txt", "r", encoding='utf-8') as fn:
        text = fn.read()# Example usage:

    text = """['\n<lrml:LegalSources>\n  <lrml:LegalSource key="ls1" sameAs="http://www.legislation.gov.in/sites/default/files/file/The%20E-Waste%20Rules%2C%202016.pdf"/>\n</lrml:LegalSources>\n\n<lrml:Context key="psInfo1">\n  <lrml:appliesAssociations>\n    <lrml:Associations>\n      <lrml:Association keyref="#ls1"/>\n      <lrml:toTarget keyref="#ps1"/>\n      <lrml:toTarget keyref="#ps2"/>\n      <lrml:toTarget keyref="#pen1"/>\n      <lrml:toTarget keyref="#pen2"/>\n    </lrml:Associations>\n  </lrml:appliesAssociations>\n</lrml:Context>\n\n<lrml:Statements key="textblock1">\n  <lrml:hasQualification>\n    <lrml:DefeasibleStrength key="str1" iri="http://defs.legalsemantics.org/defeasible-ontology/defeasible1"/>\n  </lrml:hasQualification>\n  <lrml:PrescriptiveStatement key="ps1">\n    <ruleml:Rule key=":rule1" closure="universal">\n      <lrml:if>\n        <lrml:Atom>\n          <lrml:Rel iri=":collectEWaste"/>\n          <lrml:Var>X</lrml:Var>\n        </lrml:Atom>\n      </lrml:if>\n      <lrml:then>\n        <lrml:SuborderList>\n          <lrml:Prohibition>\n            <lrml:Atom>\n              <lrml:Rel iri=":collectEWasteOnBehalfOfProducer"/>\n              <lrml:Var>X</lrml:Var>\n            </lrml:Atom>\n          </lrml:Prohibition>\n          <lrml:Prohibition>\n            <lrml:Atom>\n              <lrml:Rel iri=":collectEWasteOnBehalfOfDismantlerRefurbisherOrRecycler"/>\n              <lrml:Var>X</lrml:Var>\n            </lrml:Atom>\n          </lrml:Prohibition>\n          <lrml:Obligation>\n            <lrml:Atom>\n              <lrml:Rel iri=":ensureFacilitiesAreInAccordanceWithStandardsOrGuidelinesIssuedByCentralPollutionControlBoard"/>\n              <lrml:Var>X</lrml:Var>\n            </lrml:Atom>\n          </lrml:Obligation>\n          <lrml:Obligation>\n            <lrml:Atom>\n              <lrml:Rel iri=":ensureEWasteIsStoredInSecuredMannerTillItIsSentToAuthorisedDismantlerOrRecycler"/>\n              <lrml:Var>X</lrml:Var>\n            </lrml:Atom>\n          </lrml:Obligation>\n          <lrml:Obligation>\n            <lrml:Atom>\n              <lrml:Rel iri=":ensureNoDamageIsCausedToEnvironmentDuringStorageAndTransportationOfEWaste"/>\n              <lrml:Var>X</lrml:Var>\n            </lrml:Atom>\n          </lrml:Obligation>\n          <lrml:Obligation>\n            <lrml:Atom>\n              <lrml:Rel iri=":maintainRecordsInForm2OfEWasteHandledAsPerGuidelinesOfCentralPollutionControlBoard"/>\n              <lrml:Var>X</lrml:Var>\n            </lrml:Atom>\n          </lrml:Obligation>\n        </lrml:SuborderList>\n      </lrml:Then>\n    </ruleml:Rule>\n  </lrml:PrescriptiveStatement>\n</lrml:Statements>\n\n<lrml:PenaltyStatement key="rep1">\n  <lrml:Reparation keyref="#assoc1">\n    <lrml:appliesPenalty keyref="#pen1"/>\n    <lrml:toPrescriptiveStatement keyref="#ps1"/>\n  </lrml:Reparation>\n</lrml:PenaltyStatement>\n\n<lrml:PenaltyStatement key="rep2">\n  <lrml:Reparation keyref="#assoc1">\n    <lrml:appliesPenalty keyref="#pen2"/>\n    <lrml:toPrescriptiveStatement keyref="#ps1"/>\n  </lrml:Reparation>\n</lrml:PenaltyStatement>\n\n</lrml:Statements>']"""
    cleaned_text=text.replace('\n', '')
    print(cleaned_text)
