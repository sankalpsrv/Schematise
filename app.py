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

    paragraph_selections = session["paragraph_selections"]

    #print(paragraph_selections)

    ps_keys = []

    for paragraph_number in paragraph_selections:
        if paragraph_selections[paragraph_number] == True:
            ps_keys.append(paragraph_number)

    atoms_data, atoms_keys = extract_atoms_details(root, ps_keys)

    #print ("ps_keys is", ps_keys)

    #print(atoms_data,atoms_keys)

    ## Hereunder, combining both the dictionaries



    for key in atoms_data:
        atoms_data[key].extend(atoms_keys[key])


    print ("atoms_data combined is", atoms_data)

    tree = parse_xml_file_lxml("XML+validation/Modified-XML.xml")

    additional_elements = check_for_additional_elements_lxml(tree, atoms_data)

    print(additional_elements, "are the additional_alements generated")

    additional_elements_applicable = {}



    for key_of_additional_elements, value_of_additional_elements in additional_elements.items():
        key_trimmed = ''
        key_trimmed += key_of_additional_elements.split('_')[0]
        if key_trimmed in ps_keys:
            atoms_data[key_trimmed].append(value_of_additional_elements)

    print ("additional_elements_applicable", additional_elements_applicable)

    for key, value in additional_elements_applicable.items():
        if atoms_data[key] is not None:
            print("value is", value)
            atoms_data[key].append(value)

    print ("atoms_data with additional_elements", atoms_data)

        ## conditions_selected is created hereunder by filling in values from total_condition_statements if they have been selected
    conditions_applicable = {}
    for key, values_list in atoms_data.items():
        for value in values_list:
            print ("value is", value)
            if value in total_condition_statements:
                conditions_applicable[value] = total_condition_statements[value]
            if value in extra_conditions:
                conditions_applicable[value] = extra_conditions[value]
                print("extra_condition added", extra_conditions[value])


    #print (conditions_selected)

    if request.method == "POST":
        conditions_selected = {}

        for key in conditions_applicable.keys():
            # request.form.get returns None if the key is not present, indicating an unchecked box
            conditions_selected[key] = bool(request.form.get(key))

        print("Conditions selected are", conditions_selected)
        print("Conditions applicable are", conditions_applicable)

        conditions_met = []
        # Iterate through each key-value pair in dict1
        for key, values in atoms_data.items():
            # Check if all values for this key are True in dict2
            if all(conditions_selected.get(value, False) for value in values):
                # If all values are True, add the key to the satisfied keys list
                conditions_met.append(key)

        print ("Conditions met are", conditions_met)

        return render_template("conditions.html", conditions_applicable=conditions_applicable, additional_elements_applicable=additional_elements_applicable, conditions_met=conditions_met, total_obligation_statements=total_obligation_statements)

    return render_template("conditions.html", conditions_applicable = conditions_applicable, additional_elements_applicable=additional_elements_applicable)


