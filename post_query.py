
import urllib3
import simplejson


http = urllib3.PoolManager()

query = 'critic'
http_query = 'http://localhost:8983/solr/cisi_db/select?indent=on&q=content:' + query + '&wt=json'

response = http.request('GET', http_query)

print(response.status)

json = simplejson.loads(response.data.decode('utf-8'))
print(json['response']['numFound'], "documents found.")
# print(json['response']['docs'][0]['content'])