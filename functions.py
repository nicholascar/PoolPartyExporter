# PoolParty wiki: https://grips.semantic-web.at/display/POOLDOKU/PoolParty%27s+SPARQL+Endpoint

import requests
import json


def create_authed_session(using_proxy):
    creds = json.load(open('creds.json'))

    s = requests.Session()
    if using_proxy:
        proxies = {
            "http": 'http://' + creds['ga_usr'] + ':' + creds['ga_pwd'] + '@' + creds['ga_proxy'],
            "https": 'https://' + creds['ga_usr'] + ':' + creds['ga_pwd'] + '@' + creds['ga_proxy'],
        }
        s.proxies = proxies

    s.auth = (creds['ands_usr'], creds['ands_pwd'])  # BASIC auth

    return s


def project_has_changed(project_id, changed_since_date, using_proxy):
    URI_TEMPLATE = 'https://{SERVER}/PoolParty/sparql/{PROJECT-ID}'
    sparql_uri = URI_TEMPLATE\
        .replace('{SERVER}', json.load(open('creds.json'))['ands_server'])\
        .replace('{PROJECT-ID}', project_id)

    s = create_authed_session(using_proxy)

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


def pull_vocab(project_id, result_path, using_proxy):
    URI_TEMPLATE = 'https://{SERVER}/PoolParty/api/projects/{PROJECT-ID}/export'
    download_uri = URI_TEMPLATE\
        .replace('{SERVER}', json.load(open('creds.json'))['ands_server'])\
        .replace('{PROJECT-ID}', project_id)

    s = create_authed_session(using_proxy)
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


def read_only_sparql_query(project_id, sparql_query, using_proxy):
    URI_TEMPLATE = 'https://{SERVER}/PoolParty/sparql/{PROJECT-ID}'
    sparql_uri = URI_TEMPLATE\
        .replace('{SERVER}', json.load(open('creds.json'))['ands_server'])\
        .replace('{PROJECT-ID}', project_id)

    s = create_authed_session(using_proxy)

    params = {
        'query': '''
            ''' + sparql_query + '''
        ''',
        'format': 'application/json'
    }
    s.params = params
    r = s.get(sparql_uri)
    return json.loads(r.content)['results']['bindings']


def make_html_select_from_sparql_result(sparql_result_dict):
    html = '<select id="voc-concepts" name="voc-concepts">\n'
    for concept in sparql_result_dict:
        html += '\t<option value="' + concept['Concept']['value'] + '">' + concept['prefLabel']['value'] + '</option>\n'
    html += '</select>\n'

    return html


SPARQL_GET_ALL_CONCEPTS_URIS_AND_PREFLABELS = '''
    PREFIX skos:<http://www.w3.org/2004/02/skos/core#>
    SELECT DISTINCT ?Concept ?prefLabel
    WHERE {
        ?Concept a skos:Concept ;
            skos:prefLabel ?prefLabel .
    } ORDER BY ?prefLabel
'''


def query_sissvoc_sparql(sparql_endpoint, sparql_query):
    params = {'query': sparql_query}
    headers = {'Accept': 'application/json'}
    r = requests.get(sparql_endpoint, params=params, headers=headers)
    return json.loads(r.content)['results']['bindings']