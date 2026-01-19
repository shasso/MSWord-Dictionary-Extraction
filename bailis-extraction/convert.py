#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from utils import *


# In[ ]:


# input exmples:
# {"outside_parts": ["ܡܫܲܕܪܘܼܬܵܐ ܕܝܼܦܠܘܿܡܵܛܝܼܩܵܝܬܵܐ"], "inside_elements": [["", "ܢ", ".", "ܫܕܪ", ""]]}
# {"outside_parts": [" ܩܲܝܘܼܡܘܼܬܵܐ"], "inside_elements": [["", "ܢ", ".", "ܩܡ", ""]]}
# arg = {"entry": text, "pos": pos, "trait": {"name": name, "value": value}, "sem_domain": sem_domain_trait_value}
# Specify the file path
# file_path = "./data/entry.xml"
# write_entry_tofile(my_tree, file_path)

def NP_Processor(x):
    # make sure to extract all elements in the input
 #   lexemes = x["outside_parts"]
 #   for w in lexemes:
 #       print(w)
    print("NP Processor")
    print(x)
    en_definition = x["entry"]
    pos = x["pos"]
    trait_name = x["trait"]["name"]
    trait_value = x["trait"]["value"]
    sem_domain = x["sem_domain"]
    bib = "bailis"
    
    # lexeme is a list of dictionaries
    lexemes = x["lexemes"]
    
    # entry(aii_lexeme, en_definition, gram_info, bib, morph_type="stem", sem_domain=None)
    for item in lexemes:
        aii_lexeme = json.loads(item)["outside_parts"][0].strip()
        xx, my_tree = entry(aii_lexeme, en_definition, pos, bib, morph_type = trait_value, sem_domain = sem_domain)
        # xmlToString(xx)
        write_entry_tofile(my_tree, file_path)
    


# In[ ]:


def VP_Processor(x):
    return
    print("VP Processor")
    print(x)


# In[ ]:


def Adj_Processor(x):
    return
    print("Adjective Processor")
    print(x)


# In[ ]:


def Adv_Processor(x):
    return
    print("Adverb Processor")
    print(x)


# In[ ]:


def Other_Processor(x):
    return
    print("other Processor")
    print(x)


# In[ ]:


def parser(input_lexicon, head = None): 
    count = 0
    errors = 0
    sem_domain_trait_name = ""
    sem_domain_trait_value = ""
    pos = ""
    trait = ""
    value = ""
    result_syr = ""
    result_ar = ""
    # Parse the XML file
    tree = ET.parse(input_lexicon)
    root = tree.getroot()
    # Find all <entry> elements
    entry_elements = root.findall(".//entry")
    
    command = {}
    command["noun"] = POS_Processor(NP_Processor)
    command["verb"] = POS_Processor(VP_Processor)
    command["adjective"] = POS_Processor(Adj_Processor)
    command["adverb"] = POS_Processor(Adv_Processor)
    command["other"] = POS_Processor(Other_Processor)
    processed_counters = {"noun": 0, "verb": 0, "adjective": 0, "adverb": 0, "other": 0}
    
    pos_list = {}
    for entry in entry_elements:
        # find 
        try:
            text =  entry.find('lexical-unit/form/text').text
            trait = entry.find('trait')
            name = trait.attrib["name"]
            value = trait.attrib["value"]
            try:
                pos = entry.find('sense/grammatical-info').attrib['value']
                syr_def = entry.find('sense/definition/form[@lang="qaa-x-syr"]/text').text
                ar_def = entry.find('sense/definition/form[@lang="acm"]/text').text
            except AttributeError as e:
                errors += 1
            try:
                sem_domain_trait_name = entry.find('sense/trait').attrib['name']
                sem_domain_trait_value = entry.find('sense/trait').attrib['value']
            except AttributeError as e:
                errors += 1

            try:
                # split the strings
                result_syr = re.split(r'[؛]', syr_def)
                result_ar = re.split(r'[.]', ar_def)
            except re.error as e:
                # print(f"Regular expression error: {e}")
                errors += 1
            except Exception as e:
                # print(f"An unexpected error occurred: {e}")
                errors += 1


            # print(f'entry: {text}, pos: {pos}, trait: (name:{name},  value:{value})\n syr_def:{syr_def}\n ar_def: {ar_def} \n {sem_domain_trait_name} = {sem_domain_trait_value}')
            # Extracts all words in the list and excludes words that are in parentheses including the parentheses.
            # updated_list_of_strings = remove_parentheses_from_list(list_of_strings)
            ## extracted_words = remove_parentheses_from_list(result_syr);
            ## print(extracted_words)
            # words = result_syr.split('؛')
            arg = {"entry": text, "pos": pos, "trait": {"name": name, "value": value}, "sem_domain": sem_domain_trait_value}
            lexemes_list = []
            for input_string in result_syr:
                result_json = extract_outside_and_inside(input_string)
                # print(result_json)
                lexemes_list.append(result_json)
            arg["lexemes"] = lexemes_list
            # NP_Processor(json.dumps(arg, ensure_ascii=False))
            if "noun" in pos.lower():
                command["noun"].apply_function(arg)
                processed_counters["noun"] += 1
            elif "verb" in pos.lower():
                command["verb"].apply_function(arg)
                processed_counters["verb"] += 1                                  
            elif "adjective" in pos.lower():
                command["adjective"].apply_function(arg)
                processed_counters["adjective"] += 1
            elif "adverb" in pos.lower():
                command["adverb"].apply_function(arg)
                processed_counters["adverb"] += 1
            else:
                command["other"].apply_function(arg)
                processed_counters["other"] += 1
        
            if pos in pos_list:
                pos_list[pos] += 1
            else:
                pos_list[pos] = 1
                
            ## extracted_words.clear()
            ## extracted_words = remove_parentheses_from_list(result_ar);
            ## print(extracted_words)
            # words = result_ar.split('.')
            for input_string in result_ar:
                result_json = extract_outside_and_inside(input_string)
                # print(result_json)

            count += 1
            # print(f'count: {count}*****************')

        except ET.ParseError as e:
            # print(f"XML parsing error: {e}")
            errors += 1
            # print(f"AttributeError: {e}")
        
        if head is not None:
            if head <= 1:
                break
            else:
                head -= 1
        # need to reset key variables, it seems old values which are not updated by find, are retaining their old values.
        # arg = {"entry": text, "pos": pos, "trait": {"name": name, "value": value}, "sem_domain": sem_domain_trait_value}
        text = ""
        pos = ""
        name = ""
        value = ""
        trait = ""
        sem_domain_trait_name = ""
        sem_domain_trait_value = ""
        result_syr = ""
        result_ar = ""
        syr_def = ""
        result_ar = ""        
        
    print(f'entry count: {count}, errors: {errors}')
    print(pos_list)
    print(processed_counters)


# In[ ]:


# bailis_lexicon = './data/sample_bailis.xml'
bailis_lexicon = './data/BailisFullDictionary.lift'


# In[ ]:


# get_ipython().run_cell_magic('timeit', '', 'parser(bailis_lexicon)\n')
parser(bailis_lexicon)
