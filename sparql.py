# PoolParty wiki: https://grips.semantic-web.at/display/POOLDOKU/PoolParty%27s+SPARQL+Endpoint

import requests
import json
from datetime import datetime
import pytz


def project_has_changed(project_id, changed_since_date):
    URI_TEMPLATE = 'https://{SERVER}/PoolParty/sparql/{PROJECT-ID}'
    ands_server = 'editor.vocabs.ands.org.au'
    sparql_uri = URI_TEMPLATE\
        .replace('{SERVER}', ands_server)\
        .replace('{PROJECT-ID}', project_id)

    creds = json.load(open('creds.json'))

    s = requests.Session()
    proxies = {
        "http": 'http://' + creds['ga_usr'] + ':' + creds['ga_pwd'] + '@' + creds['ga_proxy'],
        "https": 'https://' + creds['ga_usr'] + ':' + creds['ga_pwd'] + '@' + creds['ga_proxy'],
    }
    s.proxies = proxies
    s.auth = (creds['ands_usr'], creds['ands_pwd'])  # BASIC auth
    params = {
        'query': '''
            PREFIX his: <http://schema.semantic-web.at/ppt/history#>
            PREFIX cs: <http://purl.org/vocab/changeset/schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

            SELECT ?cd
            WHERE {
              ?he cs:createdDate ?cd .
              FILTER(regex(STR(?he), "^historyEvent") ) .
              FILTER(?cd > "''' + changed_since_date.strftime('%Y-%m-%dT%H:%M:%SZ') + '''"^^xsd:dateTime)
            }
            ORDER BY DESC(?cd)
            LIMIT 1
        ''',
        'format': 'application/json'
    }
    s.params = params
    r = s.get(sparql_uri)
    changed = False
    for result in json.loads(r.content)['results']['bindings']:
        changed = True

    return changed

project_id = 'GACGIOtherVocabs'
changed_since_date = datetime(2016, 4, 1, 0, 0, 0, 0, pytz.utc)
print '---'
print project_has_changed(project_id, changed_since_date)