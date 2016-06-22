import functions
from datetime import datetime
import pytz

#
#   download a vocab if it's been changed since a dertain date
#
'''
project_id = 'GAUoM'
using_proxy = False
changed_since_date = datetime(2016, 4, 1, 0, 0, 0, 0, pytz.utc)
print 'Checking ' + project_id + '...'
if functions.project_has_changed(project_id, changed_since_date, using_proxy):
    print 'Changes detected'
    print 'Downloading ' + project_id
    functions.pull_vocab(project_id, project_id + '.ttl', using_proxy)
    print 'Complete'
else:
    print 'No changes detected'
'''

#
#   run a SPARQL query against a vocab
#
'''
project_id = 'GADynamicData'
using_proxy = False
query = functions.SPARQL_GET_ALL_CONCEPTS_URIS_AND_PREFLABELS
query_results = functions.read_only_sparql_query(project_id, query, using_proxy)
html = functions.make_html_select_from_sparql_result(query_results)
print html
'''


#
#   Query a vocab by the ANDS SISSVoc endpoint
#
sparql_endpoint = 'http://vocabs.ands.org.au/repository/api/sparql/ga_geoscience-australia-vocabulary-dynamic-data_dynamic-data-v0-1'
sparql_endpoint = 'http://vocabs.ands.org.au/repository/api/sparql/gcmd-sci'
sparql_query = functions.SPARQL_GET_ALL_CONCEPTS_URIS_AND_PREFLABELS
query_results = functions.query_sissvoc_sparql(sparql_endpoint, sparql_query)
html = functions.make_html_select_from_sparql_result(query_results)
print html