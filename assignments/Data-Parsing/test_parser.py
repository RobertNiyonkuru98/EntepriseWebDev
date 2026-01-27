import os
from main import xmlParsing

script_dir = os.path.dirname(os.path.abspath(__file__))

xml_path = os.path.join(script_dir, "modified_sms_v2.xml")
data = xmlParsing(xml_path)
print(f"Total records parsed: {len(data)}")
if data:
    print("First record sample:", data[0])