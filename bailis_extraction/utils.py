import xml.etree.ElementTree as ET
import xml.dom.minidom

# itility functions
import datetime
def get_current_date_time():

    # Get the current date and time
    current_datetime = datetime.datetime.now()

    # Format the datetime object
    formatted_datetime = current_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")

    return(formatted_datetime)

import uuid
def generate_uuid():
    # Generate a random UUID (version 4)
    generated_uuid = uuid.uuid4()

    # Convert the UUID to a string
    uuid_str = str(generated_uuid)

    return(uuid_str)

def insert_string_at_second_position(main_string, string_to_insert, source_id=""):
    return main_string[:1] +  '_' + string_to_insert + main_string[1:] + source_id;
    # return string_to_insert + '_' + main_string


# the next two functions is to normalize a string as following:
# input: ['ܨܵܡܘܿܬܵܐ(ܕ.)، ܨܵܡܘܿܬܬܵܐ(ܢ.ܨܡܬ)؛ ܫܲܠܝܵܐ(ܕ.ܫܠܐ)؛ ܫܲܬܝܼܩܵܐ(ܕ.)، ܫܵܬܘܿܩܵܐ(ܕ.ܫܬܩ)؛ ܡܵܪܹܐ ܟܝܵܢܵܐ ܫܸܠܝܵܐ(ܕ.)؛ ܠܵܐ ܠܸܫܵܢܵܢܵܐ(ܕ.ܠܫܢ)؛ ܠܵܐ ܗܲܡܙܸܡܵܢܵܐ(ܕ.ܗܡܙܡ)']
# output: ['ܨܵܡܘܿܬܵܐ، ܨܵܡܘܿܬܬܵܐ؛ ܫܲܠܝܵܐ؛ ܫܲܬܝܼܩܵܐ، ܫܵܬܘܿܩܵܐ؛ ܡܵܪܹܐ ܟܝܵܢܵܐ ܫܸܠܝܵܐ؛ ܠܵܐ ܠܸܫܵܢܵܢܵܐ؛ ܠܵܐ ܗܲܡܙܸܡܵܢܵܐ']
# basically removing anything in the parentheses

import re
def remove_parentheses(text):
    """Removes parentheses and the text within them from a string.

  Args:
    text: A string.

  Returns:
    A string with the parentheses and the text within them removed.
  """
    return re.sub(r'\([^()]*\)', '', text)

def remove_parentheses_from_list(list_of_strings):
    
    """Removes parentheses and the text within them from each string in a list of strings.

  Args:
    list_of_strings: A list of strings.

  Returns:
    A list of strings with the parentheses and the text within them removed.
  """
    updated_list_of_strings = []
    for string in list_of_strings:
        updated_list_of_strings.append(remove_parentheses(string))
    
    return updated_list_of_strings

# this function transform strings as follows:
# input: 'ܨܵܡܘܿܬܵܐ(ܕ.)، ܨܵܡܘܿܬܬܵܐ(ܢ.ܨܡܬ)؛ ܫܲܠܝܵܐ(ܕ.ܫܠܐ)؛ ܫܲܬܝܼܩܵܐ(ܕ.)، ܫܵܬܘܿܩܵܐ(ܕ.ܫܬܩ)؛ ܡܵܪܹܐ ܟܝܵܢܵܐ ܫܸܠܝܵܐ(ܕ.)؛ ܠܵܐ ܠܸܫܵܢܵܢܵܐ(ܕ.ܠܫܢ)؛ ܠܵܐ ܗܲܡܙܸܡܵܢܵܐ(ܕ.ܗܡܙܡ)'
''' output: 
{"outside_parts": ["ܨܵܡܘܿܬܵܐ", " ܨܵܡܘܿܬܬܵܐ"], "inside_elements": [["", "ܕ", "."], ["", "ܢ", ".", "ܨܡܬ", ""]]}
{"outside_parts": [" ܫܲܠܝܵܐ"], "inside_elements": [["", "ܕ", ".", "ܫܠܐ", ""]]}
{"outside_parts": [" ܫܲܬܝܼܩܵܐ", " ܫܵܬܘܿܩܵܐ"], "inside_elements": [["", "ܕ", "."], ["", "ܕ", ".", "ܫܬܩ", ""]]}
{"outside_parts": [" ܡܵܪܹܐ ܟܝܵܢܵܐ ܫܸܠܝܵܐ"], "inside_elements": [["", "ܕ", "."]]}
{"outside_parts": [" ܠܵܐ ܠܸܫܵܢܵܢܵܐ"], "inside_elements": [["", "ܕ", ".", "ܠܫܢ", ""]]}
{"outside_parts": [" ܠܵܐ ܗܲܡܙܸܡܵܢܵܐ"], "inside_elements": [["", "ܕ", ".", "ܗܡܙܡ", ""]]}

usage:
# Example usage--USE THIS ONE 
list_of_strings = 'ܨܵܡܘܿܬܵܐ(ܕ.)، ܨܵܡܘܿܬܬܵܐ(ܢ.ܨܡܬ)؛ ܫܲܠܝܵܐ(ܕ.ܫܠܐ)؛ ܫܲܬܝܼܩܵܐ(ܕ.)، ܫܵܬܘܿܩܵܐ(ܕ.ܫܬܩ)؛ ܡܵܪܹܐ ܟܝܵܢܵܐ ܫܸܠܝܵܐ(ܕ.)؛ ܠܵܐ ܠܸܫܵܢܵܢܵܐ(ܕ.ܠܫܢ)؛ ܠܵܐ ܗܲܡܙܸܡܵܢܵܐ(ܕ.ܗܡܙܡ)'
words = list_of_strings.split('؛')
for input_string in words:
    result_json = extract_outside_and_inside(input_string)
    print(result_json)

output as seen in header above.
'''
import re
import json

def extract_outside_and_inside(input_string):
    # 1. Keep each '،' separated part in a JSON object together
    parts = re.split(r'،', input_string)
    
    # 2. Extract each element inside the parentheses and parse words with diacritics
    inside_matches = re.findall(r'\(([^)]*)\)', input_string)
    inside_words = [re.split(r'(\w+)', inside) for inside in inside_matches]

    # 3. Aggregate the results into a JSON object
    result = {
 #       'outside_parts': parts,
        'outside_parts': remove_parentheses_from_list(parts),
        'inside_elements': inside_words
    }

    return json.dumps(result, ensure_ascii=False)

# generate target xml entry elemen
def entry(aii_lexeme, en_definition, gram_info, bib, morph_type="stem", sem_domain="", senses=None):
    """
    Create an <entry> element. Supports a single sense (back‑compatible) or multiple senses.

    Parameters
    ----------
    aii_lexeme : str
        The lexical unit text (AII language).
    en_definition : str
        Definition for the first sense (used when ``senses`` is None).
    gram_info : str
        Grammatical info for the first sense (used when ``senses`` is None).
    bib : str
        Bibliography text for the first sense (used when ``senses`` is None).
    morph_type : str, optional
        Value for the ``morph-type`` trait. Default ``"stem"``.
    sem_domain : str, optional
        Semantic domain for the first sense (used when ``senses`` is None).
    senses : list of dict, optional
        Each dict may contain the keys ``gram_info``, ``definition``, ``bib``, ``sem_domain``.
        When provided, the function will create one <sense> element per dict and ignore the
        ``en_definition``, ``gram_info``, ``bib`` and ``sem_domain`` arguments.

    Returns
    -------
    tuple
        (xml_string, ElementTree) where ``xml_string`` is the serialized XML for the entry.
    """
    # Create the root element
    root = ET.Element("entry")
    root.set("dateCreated", get_current_date_time())
    root.set("dateModified", get_current_date_time())
    _id = generate_uuid()
    root.set("id", insert_string_at_second_position(_id, aii_lexeme, "_bailis"))
    root.set("guid", _id)

    # Add lexical-unit
    lexical_unit = ET.SubElement(root, "lexical-unit")
    form = ET.SubElement(lexical_unit, "form")
    form.set("lang", "aii")
    text = ET.SubElement(form, "text")
    text.text = aii_lexeme

    # Morph type trait
    trait = ET.SubElement(root, "trait")
    trait.set("name", "morph-type")
    trait.set("value", morph_type)

    # Helper to create a sense element
    def _create_sense(parent, sense_data):
        sense = ET.SubElement(parent, "sense")
        sense.set("id", generate_uuid())
        sense.set("order", str(sense_data.get("order", 0)))

        grammatical_info = ET.SubElement(sense, "grammatical-info")
        grammatical_info.set("value", sense_data["grammatical-info"])

        definition = ET.SubElement(sense, "definition")
        form_def = ET.SubElement(definition, "form")
        form_def.set("lang", "en")
        text_def = ET.SubElement(form_def, "text")
        text_def.text = sense_data["definition"]

        # reversal
        reversal = ET.SubElement(sense, "reversal")
        reversal.set("type", "en")
        reversal_form = ET.SubElement(reversal, "form")
        reversal_form_text = ET.SubElement(reversal_form, "text")
        reversal_form_text.text = sense_data["definition"]
        reversal_form.set("lang", "en")
        reversal_gram_info = ET.SubElement(reversal, "grammatical-info")
        reversal_gram_info.set("value", sense_data["grammatical-info"])

        # bibliography note
        bib_info = ET.SubElement(sense, "note")
        bib_info.set("type", "bibliography")
        bib_info_form = ET.SubElement(bib_info, "form")
        bib_info_form.set("lang", "en")
        bib_text = ET.SubElement(bib_info_form, "text")
        bib_text.text = sense_data["bib"]

        # optional semantic domain
        if sense_data.get("semantic-domain"):
            semantic_domain = ET.SubElement(sense, "trait")
            semantic_domain.set("name", "semantic-domain-ddp4")
            semantic_domain.set("value", sense_data["semantic-domain"])

    # Determine senses to create
    if senses:
        for idx, s in enumerate(senses):
            s_data = {
                "grammatical-info": s.get("gram_info", ""),
                "definition": s.get("definition", ""),
                "bib": s.get("bib", ""),
                "semantic-domain": s.get("sem_domain", ""),
                "order": idx
            }
            _create_sense(root, s_data)
    else:
        # Back‑compatible single‑sense handling
        sense_data = {
            "grammatical-info": gram_info,
            "definition": en_definition,
            "bib": bib,
            "semantic-domain": sem_domain,
            "order": 0
        }
        _create_sense(root, sense_data)

    # Serialize the XML to a string
    xml_string = ET.tostring(root, encoding="utf-8").decode()
    tree = ET.ElementTree(root)
    return xml_string, tree

    # Create the root element
    root = ET.Element("entry")
    root.set("dateCreated", get_current_date_time())
    root.set("dateModified", get_current_date_time())
    _id = generate_uuid()
    root.set("id", insert_string_at_second_position(_id, aii_lexeme, "_bailis"))
    root.set("guid", _id)

    # Add child elements
    lexical_unit = ET.SubElement(root, "lexical-unit")
    form = ET.SubElement(lexical_unit, "form")
    form.set("lang", "aii")
    text = ET.SubElement(form, "text")
    text.text = aii_lexeme

    trait = ET.SubElement(root, "trait")
    trait.set("name", "morph-type")
    trait.set("value", morph_type)

    # Add sense elements
    sense_data = {
        "id": generate_uuid(),
        "order": "0",
        "grammatical-info": gram_info,
        "definition": en_definition,
        "trait_name": "semantic-domain-ddp4",
        "trait_value": sem_domain,
        "bib_text": bib,
    }

    
    sense = ET.SubElement(root, "sense")
    sense.set("id", sense_data["id"])
    sense.set("order", sense_data["order"])

    grammatical_info = ET.SubElement(sense, "grammatical-info")
    grammatical_info.set("value", sense_data["grammatical-info"])

    definition = ET.SubElement(sense, "definition")
    form = ET.SubElement(definition, "form")
    form.set("lang", "en")
    text = ET.SubElement(form, "text")
    text.text = sense_data["definition"]

    # add reversal
    reversal = ET.SubElement(sense, "reversal")
    reversal.set("type", "en")
    reversal_form = ET.SubElement(reversal, "form")
    reversal_form_text = ET.SubElement(reversal_form, "text")
    reversal_form_text.text = sense_data["definition"]
    reversal_form.set("lang", "en")
    reversal_gram_info = ET.SubElement(reversal, "grammatical-info")
    reversal_gram_info.set("value", sense_data["grammatical-info"])

    # add bib
    bib_info = ET.SubElement(sense, "note")
    bib_info.set("type", "bibliography")
    bib_info_form = ET.SubElement(bib_info, "form")
    bib_info_form.set("lang", "en")
    bib_text = ET.SubElement(bib_info_form, "text")
    bib_text.text = sense_data["bib_text"]

    if len(sem_domain) != 0:
        semantic_domain = ET.SubElement(sense, "trait")
        semantic_domain.set("name", sense_data["trait_name"])
        semantic_domain.set("value", sense_data["trait_value"])                             
        
    
    # Create an ElementTree
    tree = ET.ElementTree(root)
    
    # Serialize the XML to a string
    xml_string = ET.tostring(root, encoding="utf-8").decode()
    # print(xml_string)
    return xml_string, tree

def write_entry_tofile(root, file_path, xml_decl=False):
    # Write the XML data to the file
    with open(file_path, "ab") as file:
        root.write(file, encoding="utf-8", xml_declaration=xml_decl)

    print(f"XML data has been written to {file_path}")
 
 # Serialize the XML to a string
# xml_string = ET.tostring(root, encoding="utf-8").decode()
def xmlToString(xml_string):
    # Pretty print the XML
    dom = xml.dom.minidom.parseString(xml_string)
    pretty_xml = dom.toprettyxml()

    print(pretty_xml)
    


class POS_Processor:
    def __init__(self, function=None):
        self.function = function

    def set_function(self, function):
        self.function = function  
        
    def apply_function(self, argument):
        """Applies the set function to an argument.

        Args:
            argument: The argument to apply the function to.

        Returns:
            The result of applying the function to the argument.
        """

        if self.function is None:
            raise Exception("No function has been set.")

        return self.function(argument)
    

# define global variables here
file_path = "./data/output.lift"