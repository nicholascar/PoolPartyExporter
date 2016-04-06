# PoolParty wiki: https://grips.semantic-web.at/display/POOLDOKU/PoolParty%27s+SPARQL+Endpoint


import requests
from requests.auth import HTTPProxyAuth
import json
from SPARQLWrapper import SPARQLWrapper, JSON


URI_TEMPLATE = 'https://{SERVER}/PoolParty/sparql/{PROJECT-ID}'

ands_server = 'editor.vocabs.ands.org.au'
eg_project_id = 'GACGIOtherVocabs'
sparql_uri = URI_TEMPLATE\
    .replace('{SERVER}', ands_server)\
    .replace('{PROJECT-ID}', eg_project_id)

creds = json.load(open('creds.json'))
auth = HTTPProxyAuth(creds['usr'], creds['pwd'])


print sparql_uri
query = '''
    SELECT *
    WHERE {
        ?s ?p ?o
    }
'''
s = requests.Session()
params = {
    'query': query,
    'format': 'application/json'
}
r = s.get(sparql_uri, params=params, proxies=creds['proxy'], auth=auth)
print r

"""
from SPARQLWrapper import SPARQLWrapper, JSON, DIGEST

sparql = SPARQLWrapper("http://example.org/sparql")

sparql.setHTTPAuth(DIGEST)
sparql.setCredentials('login', 'password')

sparql.setQuery("...")
sparql.setReturnFormat(JSON)

results = sparql.query().convert()
"""

"""
sparql = SPARQLWrapper(sparql_uri)
sparql.setQuery('''
    SELECT *
    WHERE {
        ?s ?p ?o
    }
''')
sparql.setReturnFormat(JSON)
sparql.setCredentials(user=creds['usr'], passwd=creds['pwd'])
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(result["label"]["value"])
"""