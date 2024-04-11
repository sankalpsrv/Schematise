
import xml.etree.ElementTree as ET
from lxml import etree

# prompts in https://chat.openai.com/share/df33c499-2daf-4161-a796-2d3e082fdd9a
namespace_map = {
    'lrml': 'http://docs.oasis-open.org/legalruleml/ns/v1.0/',
    'ruleml': 'http://ruleml.org/spec'
}

def parse_xml_file(xml_file_path):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    return root

def parse_xml_file_lxml(xml_file_path):

    tree = etree.parse(xml_file_path)  # If you have an XML file
    return tree

def extract_atoms_details(xml_root, ps_keys):
    # Initialize dictionaries to store the results
    atoms_data_dict = {}
    atoms_keys_dict = {}

    # Find all prescriptive statements
    prescriptive_statements = xml_root.findall('.//lrml:PrescriptiveStatement', namespaces=namespace_map)

    for ps in prescriptive_statements:
        # Extract the key of the prescriptive statement
        ps_key = ps.get('key')

        # Initialize lists to store the extracted data for this prescriptive statement
        iri_values = []
        atom_keys = []

        if ps_key in ps_keys:

            # Find all <atom> blocks within <ruleml:if> blocks of the current prescriptive statement
            atoms = ps.findall('.//ruleml:if//ruleml:Atom', namespaces=namespace_map)

            for atom in atoms:
                # Extract the iri value from the <rel> tag
                rel = atom.find('.//ruleml:Rel', namespaces=namespace_map)
                if rel is not None and rel.get('iri'):
                    iri_values.append(rel.get('iri'))

                # Extract the key or keyref from the <atom> tag, if present
                if atom.get('key'):
                    atom_keys.append(atom.get('key'))
                elif atom.get('keyref'):
                    atom_keys.append(atom.get('keyref'))

            # Store the extracted iri values and atom keys in the respective dictionaries
            atoms_data_dict[ps_key] = iri_values
            atoms_keys_dict[ps_key] = atom_keys

    return atoms_data_dict, atoms_keys_dict

def extract_then_details(xml_root):
    # Initialize dictionaries to store the results for obligations and prohibitions
    obligations_dict = {}
    prohibitions_dict = {}

    # Find all prescriptive statements
    prescriptive_statements = xml_root.findall('.//lrml:PrescriptiveStatement', namespaces=namespace_map)

    for ps in prescriptive_statements:
        # Extract the key of the prescriptive statement
        ps_key = ps.get('key')

        # Initialize lists to store the extracted iri values for obligations and prohibitions
        obligations_iris = []
        prohibitions_iris = []

        # Find the <ruleml:then> block within the current prescriptive statement
        then_block = ps.find('.//ruleml:then', namespaces=namespace_map)
        if then_block is not None:
            # Extract all <Atom> blocks within <lrml:Obligation> and <lrml:Prohibition>
            obligation_atoms = then_block.findall('.//lrml:Obligation//ruleml:Atom//ruleml:Rel', namespaces=namespace_map)
            prohibition_atoms = then_block.findall('.//lrml:Prohibition//ruleml:Atom//ruleml:Rel', namespaces=namespace_map)

            # Extract iri values for obligations and prohibitions
            for atom in obligation_atoms:
                if atom.get('iri'):
                    obligations_iris.append(atom.get('iri'))

            for atom in prohibition_atoms:
                if atom.get('iri'):
                    prohibitions_iris.append(atom.get('iri'))

        # Store the extracted iri values in the respective dictionaries
        if obligations_iris:
            obligations_dict[ps_key] = obligations_iris
        if prohibitions_iris:
            prohibitions_dict[ps_key] = prohibitions_iris

    return obligations_dict, prohibitions_dict



'''def check_for_additional_elements_lxml(tree, atom_data):
    additional_elements = {}
    # Loop through each prescriptive statement key
    for ps_key, atoms in atom_data.items():
        xpath_query = f".//ruleml:Atom/ancestor::lrml:PrescriptiveStatement[@pskey='{ps_key}']/following::ruleml:if[1]"
        found_prescriptive_statements = tree.xpath(xpath_query, namespaces=namespace_map)
        for ps in found_prescriptive_statements:
            # Initialize a counter for each relationship identifier
            relationship_counter = {}
            for atom in ps.findall('.//ruleml:Atom', namespaces=namespace_map):
                relationship_identifier = "NoRel"  # Default value

                preceding_rel = atom.xpath("preceding-sibling::ruleml:Rel[@iri][1]", namespaces=namespace_map)
                if preceding_rel:
                    relationship_identifier = preceding_rel[0].get('iri')
                else:
                    if 'key' in atom.attrib:
                        relationship_identifier = atom.get('key')
                    elif 'keyref' in atom.attrib:
                        relationship_identifier = atom.get('keyref')

                # Ensure there is a unique counter for each relationship_identifier
                if relationship_identifier not in relationship_counter:
                    relationship_counter[relationship_identifier] = {}

                for child in atom:
                    original_tag_name = etree.QName(child).localname
                    # Initialize or update the count for this tag within the relationship
                    tag_count = relationship_counter[relationship_identifier].get(original_tag_name, 0) + 1
                    relationship_counter[relationship_identifier][original_tag_name] = tag_count

                    composite_tag_name = f"{ps_key}_{relationship_identifier}_{original_tag_name}_{tag_count}"

                    element_text = (child.text or '').strip()
                    if element_text:  # Ensure non-empty values
                        additional_elements[composite_tag_name] = element_text
                        print(f"Processed tag: {composite_tag_name} with text: {element_text}")

    return additional_elements

'''

def check_for_additional_elements_lxml(tree, atom_data):
    additional_elements = {}
    for ps_key, atoms in atom_data.items():
        # This XPath query looks for Atom elements that are descendants of an `if` element,
        # which is itself a descendant of a PrescriptiveStatement with the matching pskey.
        xpath_query = f".//lrml:PrescriptiveStatement[@key='{ps_key}']//ruleml:if//ruleml:Atom"
        found_atoms = tree.xpath(xpath_query, namespaces=namespace_map)

        # Initialize a counter for each Atom's relationship identifier
        relationship_counter = {}
        for atom in found_atoms:
            relationship_identifier = "NoRel"  # Default value

            # Check for preceding <Rel> or Atom's own key/keyref
            preceding_rel = atom.xpath("preceding-sibling::ruleml:Rel[@iri][1]", namespaces=namespace_map)
            if preceding_rel:
                relationship_identifier = preceding_rel[0].get('iri')
            else:
                if 'key' in atom.attrib:
                    relationship_identifier = atom.get('key')
                elif 'keyref' in atom.attrib:
                    relationship_identifier = atom.get('keyref')

            # Ensure a unique counter for each relationship_identifier
            if relationship_identifier not in relationship_counter:
                relationship_counter[relationship_identifier] = {}

            for child in atom:
                original_tag_name = etree.QName(child).localname
                # Initialize or update the count for this tag within the relationship
                tag_count = relationship_counter[relationship_identifier].get(original_tag_name, 0) + 1
                relationship_counter[relationship_identifier][original_tag_name] = tag_count

                composite_tag_name = f"{ps_key}_{relationship_identifier}_{original_tag_name}_{tag_count}"

                element_text = (child.text or '').strip()
                if element_text:  # Ensure non-empty values
                    additional_elements[composite_tag_name] = element_text
                    print(f"Processed tag: {composite_tag_name} with text: {element_text}")

    return additional_elements


if __name__ == "__main__":

    root = parse_xml_file("/media/sankalp-justify/LinuxData/sankalp-justify/Schematise-UseCase/Complianalyse-webapp/XML+validation/Modified-XML.xml")
    print("root is", root)
    ps_keys = ['paragraph2', 'paragraph3', 'paragraph4', 'paragraph5', 'paragraph6', 'paragraph7', 'paragraph8']
    # Extract data and store it in the dictionaries
    atoms_data, atoms_keys = extract_atoms_details(root, ps_keys)

    # For demonstration, print the extracted data
    print("Atoms Data Dictionary:")
    for key, value in atoms_data.items():
        print(f"Prescriptive Statement Key: {key}, IRI Values: {value}")

    print("\nAtoms Keys Dictionary:")
    for key, value in atoms_keys.items():
        print(f"Prescriptive Statement Key: {key}, Atom Keys/Keyrefs: {value}")

    # Extract data and store it in the dictionaries
    obligations_data, prohibitions_data = extract_then_details(root)

    # For demonstration, print the extracted data
    print("Obligations Dictionary:")
    for key, value in obligations_data.items():
        print(f"Prescriptive Statement Key: {key}, IRI Values: {value}")

    print("\nProhibitions Dictionary:")
    for key, value in prohibitions_data.items():
        print(f"Prescriptive Statement Key: {key}, IRI Values: {value}")

    tree = etree.parse("/media/sankalp-justify/LinuxData/sankalp-justify/Schematise-UseCase/Complianalyse-webapp/XML+validation/Modified-XML.xml")  # If you have an XML file

    # Example usage with either the atoms_data or atoms_keys dictionary
    # Let's assume we have an example atoms_data or atoms_keys dictionary ready for demonstration purposes
    example_atoms_data = {'ps1': [':exampleIRI1', ':exampleIRI2']}
    example_atoms_keys = {'ps1': ['key1', 'key2']}

    # Checking for additional elements using the atoms_data dictionary
    additional_elements_from_data = check_for_additional_elements_lxml(tree, atoms_data)
    print("Additional Elements from IRI Values Dictionary:")
    for key, value in additional_elements_from_data.items():
        print(f"Element: {key}, Value: {value}")

    # Optionally, you can check using the atoms_keys dictionary in a similar manner
    # additional_elements_from_keys = check_for_additional_elements(root, example_atoms_keys)
