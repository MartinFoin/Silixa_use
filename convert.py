import os
import pandas as pd
import xml.etree.ElementTree as ET

input_dir = 'xml_files'
output_dir = 'csv_files'

# WITSML uses namespaces, which we need to strip or handle to easily find tags
def strip_namespace(tag):
    if '}' in tag:
        return tag.split('}', 1)[1]
    return tag

for filename in os.listdir(input_dir):
    if filename.endswith('.xml'):
        xml_path = os.path.join(input_dir, filename)
        csv_path = os.path.join(output_dir, filename.replace('.xml', '.csv'))
        
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            
            # Find the mnemonic (column headers) definition
            mnemonics = []
            for elem in root.iter():
                if strip_namespace(elem.tag) == 'logCurveInfo':
                    for child in elem:
                        if strip_namespace(child.tag) == 'mnemonic':
                            mnemonics.append(child.text)
            
            # Find the actual data rows
            data_rows = []
            for elem in root.iter():
                if strip_namespace(elem.tag) == 'data':
                    # WITSML data nodes usually contain comma-separated values
                    row_values = elem.text.split(',')
                    data_rows.append(row_values)
            
            # Create a dataframe using the extracted headers and data
            if data_rows:
                # If mnemonics were found, use them as headers; otherwise, default to None
                df = pd.DataFrame(data_rows, columns=mnemonics if len(mnemonics) == len(data_rows[0]) else None)
                df.to_csv(csv_path, index=False)
                print(f"Success: {filename}")
            else:
                print(f"Skipped {filename}: No <data> tags found.")
                
        except Exception as e:
            print(f"Failed {filename}: {e}")
