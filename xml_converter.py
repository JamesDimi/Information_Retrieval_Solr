import xml.etree.ElementTree as ET


def convert_to_xml(filepath):
    root = ET.Element('add')
    root.text = '\n'  # newline before the doc element

    tagindex = 0  # used to know, with which tag we are working with

    with open(filepath) as f:

        for line in f:

            if line.startswith(".I"):

                # create a new <doc> tag
                document = ET.SubElement(root, 'doc')
                document.text = '\n'  # newline before the collected element
                document.tail = '\n'

                # create the id field
                id = ET.SubElement(document, 'field')
                id.set('name', 'id')  # set the name attribute
                idnum = [int(s) for s in line.split() if s.isdigit()]  # get the id number
                id.text = idnum[0].__str__()  # convert the id number to string
                id.tail = '\n'

            elif line.startswith(".T"):
                tagindex = 1

                title = ET.SubElement(document, 'field')
                title.set('name', 'title')  # set the name attribute
                title.set('type', 'text_en')  # set the type attribute
                title.text = "\n"  # get text ready for the input
                title.tail = '\n'  # add new line after the tag
                line = f.__next__()  # skip the current line which contains the .T / .A / .W etc

            elif line.startswith(".A"):
                tagindex = 2

                author = ET.SubElement(document, 'field')
                author.set('name', 'author')
                author.text = "\n"
                author.tail = '\n'
                line = f.__next__()

            elif line.startswith(".W") & (filepath.__contains__(".ALL")):
                tagindex = 3

                content = ET.SubElement(document, 'field')
                content.set('name', 'content')
                content.set('type', 'text_en')  # set the type attribute
                content.text = "\n"
                content.tail = '\n'
                line = f.__next__()

            elif line.startswith(".W") & (filepath.__contains__(".QRY")):
                tagindex = 4

                word = ET.SubElement(document, 'field')
                word.set('name', 'word')
                word.text = "\n"
                word.tail = '\n'
                line = f.__next__()

            elif line.startswith(".X") | line.startswith(".B"):  # ignore the .X and .B tags
                tagindex = 0  # do nothing for the following lines

            # add the text to the tags
            if tagindex == 1:
                title.text += line[:-1] + ' '
            elif tagindex == 2:
                author.text += line[:-1] + ' '
            elif tagindex == 3:
                content.text += line[:-1] + ' '
            elif tagindex == 4 and not (line.startswith(".I")):
                word.text += line[:-1] + ' '

    # Include the root element to the tree and write the tree
    # to the file.
    tree = ET.ElementTree(root)

    if filepath.__contains__(".ALL"):
        tree.write('./cisi_xml/Documents.xml', encoding='utf-8', xml_declaration=True)
    else:
        tree.write('./cisi_xml/Queries.xml', encoding='utf-8', xml_declaration=True)


# Call the function for our Collections
convert_to_xml("./cisi/CISI.ALL")  # convert the CISI.ALL to xml
convert_to_xml("./cisi/CISI.QRY")  # convert the CISI.QRY to xml