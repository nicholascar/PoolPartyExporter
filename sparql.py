# PoolParty wiki: https://grips.semantic-web.at/display/POOLDOKU/PoolParty%27s+SPARQL+Endpoint

import requests
import json
from datetime import datetime
import pytz


def create_authed_session():
    creds = json.load(open('creds.json'))

    s = requests.Session()
    proxies = {
        "http": 'http://' + creds['ga_usr'] + ':' + creds['ga_pwd'] + '@' + creds['ga_proxy'],
        "https": 'https://' + creds['ga_usr'] + ':' + creds['ga_pwd'] + '@' + creds['ga_proxy'],
    }
    s.proxies = proxies
    s.auth = (creds['ands_usr'], creds['ands_pwd'])  # BASIC auth

    return s


def project_has_changed(project_id, changed_since_date):
    URI_TEMPLATE = 'https://{SERVER}/PoolParty/sparql/{PROJECT-ID}'
    sparql_uri = URI_TEMPLATE\
        .replace('{SERVER}', json.load(open('creds.json'))['ands_server'])\
        .replace('{PROJECT-ID}', project_id)

    s = create_authed_session()

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


def pull_vocab(project_id, result_path):
    URI_TEMPLATE = 'https://{SERVER}/PoolParty/api/projects/{PROJECT-ID}/export'
    download_uri = URI_TEMPLATE\
        .replace('{SERVER}', json.load(open('creds.json'))['ands_server'])\
        .replace('{PROJECT-ID}', project_id)

    s = create_authed_session()
    s.params = {
        'format': 'Turtle',
        'exportModules': 'concepts'
    }
    r = s.get(download_uri)
    if r.status_code == 200:
        with open(result_path, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
    else:
        raise Exception('Didn\'t get an HTTP 200 for the vocab download')


project_id = 'GACGIOtherVocabs'

changed_since_date = datetime(2016, 4, 1, 0, 0, 0, 0, pytz.utc)
print 'Checking ' + project_id + '...'
if project_has_changed(project_id, changed_since_date):
    print 'Changes detected'
    print 'Downloading ' + project_id
    pull_vocab(project_id, project_id + '.ttl')
    print 'Complete'
else:
    print 'No changes detected'
