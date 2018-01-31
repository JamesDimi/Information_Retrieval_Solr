import re
import xml.etree.ElementTree as ET

import simplejson
import urllib3
import requests

# Parse the query XML
tree = ET.parse('./cisi_xml/Queries.xml')
root = tree.getroot()


# Formats the input string to compatible format with http
def clear_query(input):
    # make the input valiable for the url format
    input = re.sub("[\\t]", "", input)
    input = re.sub("^[\\n]", "", input)
    input = re.sub(":", "", input)
    input = re.sub("[\\s]", "+", input)
    input = re.sub("\(", "", input)
    input = re.sub("\)", "", input)
    input = re.sub("\"", "", input)
    input = re.sub("\'", "", input)
    input = re.sub("\*", "", input)
    input = re.sub("\/", "", input)
    input = re.sub("%", "", input)
    return input


query_doc = {}  # will be a dictionary that keeps which documents (id) is relevant
queries_post = []  # Contains the queries transformed into http, to be posted to Solr

http = urllib3.PoolManager()

for doc in root:

    # If the document has a length of 2:
    # It means that it has only the fields of {id, word)
    # or else:
    # It means that it has the fields of {id, title, author, word}
    # if len(doc) == 2:
    #     print("0", doc[0].text)
    #     print("1", doc[1].text)
    # elif len(doc) > 2:
    #     print("0", doc[0].text)
    #     print("1", doc[1].text)
    #     print("2", doc[2].text)
    #     print("3", doc[3].text)

    if len(doc) == 2:
        word = doc[1].text  # get the word
        word = clear_query(word)
        http_query = 'http://localhost:8983/solr/cisi_db/select?fl=id,score&q=content:' + word
    else:
        # Parse the field texts
        title = doc[1].text  # get the title
        author = doc[2].text  # get the author
        word = doc[3].text  # get the content

        # Make the strings compatible for the http
        title = clear_query(title)
        author = clear_query(author)
        word = clear_query(word)

        # Create the http
        http_query = 'http://localhost:8983/solr/cisi_db/select?fl=id,score&q=title:' + title + 'OR+author:' + author + 'OR+content:' + word

    http_query = http_query + '&rows=4000&wt=json'
    # print(http_query)
    queries_post.append(http_query)

query_id = 1  # Used to know in which query we currently are
out_file = open("SolrResults.txt", "w")  # Create the output file

count = 0
for query in queries_post:

    response = requests.get(query).json()
    data_array = response['response']['docs']

    response_doc_id = []
    response_doc_score = []

    for data in data_array:
        response_doc_id.append(data['id'])
        response_doc_score.append(data['score'])

    query_doc[query_id] = response_doc_id
    query_doc[query_id] = response_doc_score

    if len(response_doc_id) != 0:
        count += 1

    print("query_id:", query_id)
    print("respongs_length:", len(response_doc_id))

    for i in range(0, len(response_doc_id)):
        output2 = response_doc_id[i]
        output4 = response_doc_score[i]
        out_file.write(str(query_id) + " Q0 " + str(output2) + " 1 " + str(output4) + " STANDARD \n")
    query_id += 1
print("total answered Queries:", count)
out_file.close()
