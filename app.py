import json
import logging
import time
from datetime import datetime, timezone
from flask import Flask, g, request

app = Flask(__name__)
logger = logging.getLogger('requisicoes')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(handler)
logger.propagate = False

@app.before_request
def inicio():
    g.inicio = time.perf_counter()

@app.after_request
def registrar(response):
    logger.info(json.dumps({
        '@timestamp': datetime.now(timezone.utc).isoformat(),
        'service': 'devops', 'method': request.method, 'path': request.path,
        'status_code': response.status_code,
        'response_time_ms': round((time.perf_counter() - g.inicio) * 1000, 3)
    }))
    return response

@app.get('/')
def index():
    return {'mensagem': 'Projeto DevOps funcionando!'}

@app.get('/health')
def health():
    return {'status': 'ok'}
