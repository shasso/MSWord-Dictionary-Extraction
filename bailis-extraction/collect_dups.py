#!/usr/bin/env python
# coding: utf-8

# ## collect duplicate entries into list collections

# In[1]:


import xml.etree.ElementTree as ET

def collect_duplicate_entries(xml_file_path):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    duplicate_entries_dict = {}

    for entry in root.findall('.//entry'):
        lexical_unit = entry.find('./lexical-unit/form[@lang="aii"]/text')
        
        if lexical_unit is not None:
            text_value = lexical_unit.text

            # Check if the text value is already in the dictionary
            if text_value in duplicate_entries_dict:
                duplicate_entries_dict[text_value].append(entry)
            else:
                duplicate_entries_dict[text_value] = [entry]

    return duplicate_entries_dict

def write_duplicate_entries_to_file(duplicate_entries_dict, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for key, entries in duplicate_entries_dict.items():
            output_file.write(f"Text Value: {key}\n")
            for entry in entries:
                entry_str = ET.tostring(entry, encoding='utf-8').decode('utf-8')
                output_file.write(entry_str)
                output_file.write("\n")
            output_file.write("\n")


# In[2]:


# Replace 'your_file.xml' with the actual path to your XML file
xml_file_path = './data/output.lift'
output_file_path = './data/duplicates.xml'

duplicate_entries_dict = collect_duplicate_entries(xml_file_path)
# Now 'duplicate_entries_dict' contains a dictionary with text values as keys
# Each key maps to a list of duplicate entry elements

# Write the output to a file
write_duplicate_entries_to_file(duplicate_entries_dict, output_file_path)

# In[3]:


len(duplicate_entries_dict)


# In[5]:


type(duplicate_entries_dict)


# In[ ]:





# In[4]:


# Now 'duplicate_entries_dict' contains a dictionary with text values as keys
# Each key maps to a list of duplicate entry elements
for key, entries in duplicate_entries_dict.items():
    print(f"Text Value: {key}")
    for entry in entries:
        print(ET.tostring(entry, encoding='utf-8').decode('utf-8'))
    print("\n")


# In[ ]:




