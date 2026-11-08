import json
from unittest.mock import patch
import pytest
from app import app

@pytest.mark.parametrize('path,status', [('/', 200), ('/health', 200), ('/inexistente', 404)])
def test_respostas_e_logs(path, status):
    with patch('app.logger.info') as log:
        response = app.test_client().get(path)
    assert response.status_code == status
    event = json.loads(log.call_args.args[0])
    assert event['status_code'] == status
    assert event['path'] == path
    assert event['response_time_ms'] >= 0
    assert event['@timestamp']

def test_health():
    assert app.test_client().get('/health').json == {'status': 'ok'}
