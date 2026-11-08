"""cria objetos do kibana usando a api local. execute após iniciar o kibana."""
import json
import urllib.request

BASE = 'http://127.0.0.1:5601/api/saved_objects/'
def save(kind, ident, attributes, references=None):
    request = urllib.request.Request(BASE + kind + '/' + ident + '?overwrite=true',
        data=json.dumps({'attributes': attributes, 'references': references or []}).encode(),
        headers={'Content-Type': 'application/json', 'kbn-xsrf': 'true'}, method='POST')
    with urllib.request.urlopen(request, timeout=30) as response:
        print(kind, ident, response.status)

save('index-pattern', 'devops', {'title': 'devops-*', 'timeFieldName': '@timestamp'})
index_refs = [{'name': 'kibanaSavedObjectMeta.searchSourceJSON.index', 'type': 'index-pattern', 'id': 'devops'}]
search = json.dumps({'indexRefName': 'kibanaSavedObjectMeta.searchSourceJSON.index', 'query': {'language': 'kuery', 'query': ''}, 'filter': []})
save('search', 'devops-logs', {'title': 'Logs da aplicação',
    'columns': ['path', 'status_code', 'response_time_ms'], 'sort': [['@timestamp', 'desc']],
    'kibanaSavedObjectMeta': {'searchSourceJSON': search}}, index_refs)
for ident, title, kind, aggs in [
    ('devops-status', 'Requisições por status HTTP', 'histogram', [
        {'id': '1', 'enabled': True, 'type': 'count', 'schema': 'metric', 'params': {}},
        {'id': '2', 'enabled': True, 'type': 'terms', 'schema': 'segment', 'params': {'field': 'status_code', 'size': 10, 'order': 'desc', 'orderBy': '1'}}]),
    ('devops-tempo', 'Tempo médio de resposta (ms)', 'metric', [
        {'id': '1', 'enabled': True, 'type': 'avg', 'schema': 'metric', 'params': {'field': 'response_time_ms'}}])]:
    save('visualization', ident, {'title': title,
        'visState': json.dumps({'title': title, 'type': kind, 'params': {}, 'aggs': aggs}),
        'uiStateJSON': '{}', 'kibanaSavedObjectMeta': {'searchSourceJSON': search}}, index_refs)
panels = []
references = []
for i, (ident, kind) in enumerate([('devops-logs', 'search'), ('devops-status', 'visualization'), ('devops-tempo', 'visualization')]):
    references.append({'name': 'panel_' + str(i), 'type': kind, 'id': ident})
    panels.append({'panelIndex': str(i), 'type': kind, 'panelRefName': 'panel_' + str(i), 'version': '8.17.0',
        'gridData': {'x': 0, 'y': i * 12, 'w': 48, 'h': 12, 'i': str(i)}, 'embeddableConfig': {}})
save('dashboard', 'devops-dashboard', {'title': 'Projeto DevOps', 'panelsJSON': json.dumps(panels),
    'optionsJSON': '{}', 'timeRestore': True, 'timeFrom': 'now-15m', 'timeTo': 'now',
    'refreshInterval': {'pause': False, 'value': 5000},
    'kibanaSavedObjectMeta': {'searchSourceJSON': json.dumps({'query': {'language': 'kuery', 'query': ''}, 'filter': []})}}, references)
