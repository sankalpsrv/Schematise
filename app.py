import flask
from flask import Flask, render_template, request, redirect, url_for, session
from xml_ops import parse_xml_file, extract_atoms_details, parse_xml_file_lxml, check_for_additional_elements_lxml
from decouple import config


from conditions import total_condition_statements, total_obligation_statements, extra_conditions

# Assuming the XML parsing and namespace map from previous steps

app = Flask(__name__)
app.secret_key = config('secret_key')

def paragraph_to_condition(paragraph_selections):
    conditions_list = []


@app.route('/')
def index():

    return render_template("index.html")

@app.route('/selection', methods = ["GET", "POST"])
def selection():

    if request.method == "POST":
        # Initialize a dictionary to hold the boolean values for each paragraph
        paragraph_selections = {
            'paragraph2': False,
            'paragraph3': False,
            'paragraph4': False,
            'paragraph5': False,
            'paragraph6': False,
            'paragraph7': False,
            'paragraph8': False
        }

        # Iterate through the keys (paragraph names) in the dictionary
        for paragraph in paragraph_selections.keys():
            # Check if the paragraph checkbox was checked in the form submission
            if request.form.get(paragraph):
                # If so, set the value for that paragraph to True
                paragraph_selections[paragraph] = True

        session['paragraph_selections'] = paragraph_selections

        return redirect(url_for('obligation'))

    return render_template("selection.html")

@app.route('/obligation', methods = ["GET", "POST"])
def obligation():
    root = parse_xml_file("XML+validation/Modified-XML.xml")

    # Get the value of paragraph_selections from previous page which was saved in a cookie
    paragraph_selections = session["paragraph_selections"]

    #print(paragraph_selections)

    ps_keys = []

    #Store all prescriptive statement keys for the paragraphs selected
    for paragraph_number in paragraph_selections:
        if paragraph_selections[paragraph_number] == True:
            ps_keys.append(paragraph_number)

    # Calling the extract_atoms_details function from xml_ops.py for getting the conditions which are applicable for each of the paragraphs selected
    atoms_data, atoms_keys = extract_atoms_details(root, ps_keys)

    #print ("ps_keys is", ps_keys)

    #print(atoms_data,atoms_keys)

    ## Hereunder, combining both the dictionaries

    for key in atoms_data:
        atoms_data[key].extend(atoms_keys[key])


    print ("atoms_data combined is", atoms_data)

    # Variable named "additional_elements" gets all the additional_elements for the atoms_data whereas, <br>

    tree = parse_xml_file_lxml("XML+validation/Modified-XML.xml")

    additional_elements = check_for_additional_elements_lxml(tree, atoms_data)

    print(additional_elements, "are the additional_alements generated")


    # iterating through each of the additional elements

    for key_of_additional_elements, value_of_additional_elements in additional_elements.items():
        # splitting each additional element key to get the paragraph number
        key_trimmed = ''
        key_trimmed += key_of_additional_elements.split('_')[0]
        # checking if the paragraph number is in the paragraphs selected by the user
        if key_trimmed in ps_keys:
            # if present, appending to the list of compliances for that paragraph
            atoms_data[key_trimmed].append(value_of_additional_elements)

    print ("atoms_data with additional_elements", atoms_data)



    conditions_applicable = {}
    optional_conditions = {}
    # iterating through the keys and values of the total applicable compliances stored paragraph-wise in atoms_data
    for key, values_list in atoms_data.items():
        for value in values_list:
            print ("value is", value)
            # checks if the compliance is one that was extracted from the parent blocks of the atoms
            if value in total_condition_statements:
                # conditions_applicable holds the atomic elements with the dictionary value being the statement for compliance
                # which was extracted from the conditions.py file's variable named "total_condition_statements"
                conditions_applicable[value] = total_condition_statements[value]
            # checks if the compliance is one that was extracted from the call for check_for_additional_elements_lxml(tree,atoms_data)
            if value in extra_conditions:
                # optional_conditions holds the optional elements extracted earlier with the dictionary value being
                # the value extracted from conditions.py file's variable named "extra_conditions"
                optional_conditions[value] = extra_conditions[value]
                #print("extra_condition added", extra_conditions[value])

    print("optional_conditions", optional_conditions)

    print("applicable conditions", conditions_applicable)
    #print (conditions_selected)

    # processes form data
    if request.method == "POST":
        conditions_selected = {}

        optional_conditions_selected = {}

        # gets values for both the conditions from parent blocks and optional conditions for each paragraph
        for key in conditions_applicable.keys():
            # request.form.get returns None if the key is not present, indicating an unchecked box
            conditions_selected[key] = bool(request.form.get(key))

        for key in optional_conditions.keys():
            # request.form.get returns None if the key is not present, indicating an unchecked box
            optional_conditions_selected[key] = bool(request.form.get(key))

        print("Conditions selected are", conditions_selected, optional_conditions_selected)
        #print("Conditions applicable are", conditions_applicable, optional_conditions)

        conditions_met = []

        # Iterate through each key-value pair in atoms_data to check if any of the paragraphs' conditions are met by the checklist submitted
        for key, values in atoms_data.items():
            # Filter values to include only those that have corresponding keys in conditions_selected
            filtered_values = [value for value in values if value in conditions_selected]
            filtered_optional_values = [value for value in values if value in optional_conditions_selected]

            print("Values being checked are", filtered_values)  # Updated to print filtered values
            print ("Filtered_optional_values are", filtered_optional_values)

            # Check if all filtered values are True in conditions_selected
            if all(conditions_selected[value] for value in
                   filtered_values):  # Here we directly access the value as the existence is guaranteed
                # Check if any condition is True in optional_conditions_selected for the given values
                if any(optional_conditions_selected.get(value, False) for value in
                       filtered_optional_values):  # Using False as default if key doesn't exist
                    # If any values are True, add the key to the satisfied keys list
                    conditions_met.append(key)

                elif len(filtered_optional_values) == 0:
                    conditions_met.append(key)

        print ("Conditions met are", conditions_met)

        return render_template("conditions.html", conditions_applicable=conditions_applicable, optional_conditions=optional_conditions, conditions_met=conditions_met, total_obligation_statements=total_obligation_statements)

    return render_template("conditions.html", conditions_applicable = conditions_applicable, optional_conditions=optional_conditions)


