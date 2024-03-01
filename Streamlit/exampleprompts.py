### This is the list of examples for LangChain integration. Currently, the first two examples are for LegalRuleML and the third one is for LegalDocML

examples_legalruleml = [
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

examples_legaldocml = [
	{
	 "question": """303. Order to compel arbitration; appointment of arbitrators; locale
(a) A court having jurisdiction under this chapter may direct that arbitration be held in accordance with the agreement at any place therein provided for, whether that place is within or without the United States. The court may also appoint arbitrators in accordance with the provisions of the agreement.

(b) In the event the agreement does not make provision for the place of arbitration or the appointment of arbitrators, the court shall direct that the arbitration shall be held and the arbitrators be appointed in accordance with Article 3 of the Inter-American Convention.""",
	"answer": """<portion includedIn="/akn/us/act/title_9">
<portionBody>
            <chapter GUID="idd1d2ae15-f639-11e2-8470-abc29ba29c4d" eId="chp_3">
                <num>CHAPTER 3—</num>
                <heading>INTER-AMERICAN CONVENTION ON INTERNATIONAL COMMERCIAL ARBITRATION</heading>
                <intro>
                    <toc>
                        <tocItem href="" level="1">
                            <span>Sec.</span>
                        </tocItem>
                        <tocItem href="#sec_301" level="1">
                            <span>301.</span>
                            <span>Enforcement of Convention.</span>
                        </tocItem>
                        <tocItem href="#sec_302" level="1">
                            <span>302.</span>
                            <span>Incorporation by reference.</span>
			</tocItem>
			<tocItem href="#sec_303" level="1">
                            <span>303.</span>
                            <span>Order to compel arbitration; appointment of arbitrators; locale.</span>
                        </tocItem>
		    </toc>
		</intro>

                    
		 <section GUID="idd1d2fc3c-f639-11e2-8470-abc29ba29c4d" eId="sec_303">
                    <num>§ 303.</num>
                    <heading> Order to compel arbitration; appointment of arbitrators; locale</heading>
                    <subsection GUID="idd1d2fc3d-f639-11e2-8470-abc29ba29c4d" eId="sec_303__subsec_a">
                        <num >(a)</num>
                        <content>
                            <p> A court having jurisdiction under this chapter may direct that arbitration be held in accordance with the agreement at any place therein provided for, whether that place is within or without the United States. The court may also appoint
                                arbitrators in accordance with the provisions of the agreement.</p>
                        </content>
                    </subseection>                    
<subsection GUID="idd1d2fc3e-f639-11e2-8470-abc29ba29c4d" eId="sec_303__subsec_b">
                        <num >(b)</num>
                        <content>

                            <p> In the event the agreement does not make provision for the place of arbitration or the appointment of arbitrators, the court shall direct that the arbitration shall be held and the arbitrators be appointed in accordance with <ref href="/akn/oas/act/1975__b_35/eng@1975-01-30#art_3">Article 3 of the
                                Inter-American Convention</ref>.</p>
                        </content>
                    </subsection>
                </section>		
</chapter>
        </portionBody>
    </portion>
</akomaNtoso>
"""}

    ]
