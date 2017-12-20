
import urllib3
import simplejson


http = urllib3.PoolManager()

query = 'critic'
http_query = 'http://localhost:8983/solr/cisi_db/select?indent=on&q=content:' + query + '&wt=json'

response = http.request('GET', http_query)

query_document = {}     # will be a dictionary that keeps which documents (id) is relevant

json = simplejson.loads(response.data.decode('utf-8'))
print(json['response']['numFound'], "documents found.")

# print(json['response']['docs'][0]['content'])

# TODO: Loop over Query xml, post them via http to solr and gather the responses.
# TODO: Finally format the resposes correctly and use Trec Eval to evaluate all the responses