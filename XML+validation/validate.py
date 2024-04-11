from lxml import etree

# Load the XSD Schema
xsd_schema_doc = etree.parse('/media/sankalp-justify/LinuxData/sankalp-justify/Schematise-UseCase/Complianalyse-webapp/XML+validation/lrml-basic.xsd')
xsd_schema = etree.XMLSchema(xsd_schema_doc)

# Parse the updated XML document
xml_doc = etree.parse('/media/sankalp-justify/LinuxData/sankalp-justify/Schematise-UseCase/Complianalyse-webapp/XML+validation/Modified-XML.xml')

# Validate the XML document against the XSD Schema
is_valid = xsd_schema.validate(xml_doc)
validation_errors = xsd_schema.error_log

print(f"Is the XML valid? {is_valid}")
if not is_valid:
    print("Validation errors:")
    for error in validation_errors:
        print(error)
