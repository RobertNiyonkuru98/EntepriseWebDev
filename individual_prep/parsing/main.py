import xml.etree.ElementTree as ET

# Parse XML into Element Tree
tree = ET.parse("xml_file.xml")
root = tree.getroot()

# Root
print(root.tag)
print(len(root))

# Root Child
print(root[0].tag)
print(len(root[0]))

# Loop over root children
for child in root:
    print(child[1].tag)
    print(child[0].text)

# Root grandchildren
print(root[0][0].tag)
print(root[0][0].text)
print(root[0][1].tag)
print(root[0][1].text)

# Get an attribute
print(root.attrib)

# Loop over "Ticker" tag
for ticker in root.iter('ticker'):
    print(ticker.text)

# Find Children with 'Price' Tag
print(len(root[0].findall('price')))
print(root[0].findall('price')[0].text)

# Change Price & Remove Currency
root[0][2].text = "244"
# root[1].remove(root[1][3])
tree.write('xml_file.xml')