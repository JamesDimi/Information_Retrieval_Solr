
import re
import urllib3
import simplejson
import xml.etree.ElementTree as ET

tree = ET.parse('./cisi_xml/Queries.xml')
root = tree.getroot()

query_doc = {}     # will be a dictionary that keeps which documents (id) is relevant

http = urllib3.PoolManager()

for doc in root:
    query_id = doc[0].text        # get the query_id
    query = doc[1].text     # get the query

    # make the query valiable for the url format
    query = re.sub("[\\t]", "", query)
    query = re.sub("^[\\n]", "", query)
    query = re.sub(":", "", query)
    query = re.sub("[\\s]", "+", query)

    http_query = 'http://localhost:8983/solr/cisi_db/select?indent=on&q=content:' + query + '&wt=json'
    response = http.request('GET', http_query)

    json = simplejson.loads(response.data.decode('utf-8'))
    query_doc[query_id] = json['response']['numFound']

for query_id in query_doc:
    print(query_id, query_doc[query_id])
