# Projeto DevOps

Aplicação Flask com testes, CI/CD no GitHub Actions, deploy no Kubernetes com Helm
e logs coletados por Filebeat, Elasticsearch e Kibana.

## Executar localmente

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
flask --app app run
```

Rotas: `/` e `/health`.

## Deploy

O pipeline da branch `main` testa, publica a imagem no GHCR e faz o deploy no
cluster `kind-devops`. Requer um runner Linux com Docker, Kind, kubectl e Helm,
além do secret `GHCR_READ_TOKEN` com permissão `read:packages`.

Para executar manualmente em um cluster criado com `kind-config.yaml`:

```bash
docker build -t ghcr.io/kal-neves/projeto-devops:local .
kind load docker-image ghcr.io/kal-neves/projeto-devops:local --name devops
helm upgrade --install devops helm --kube-context kind-devops -n devops --create-namespace --wait
curl -f http://127.0.0.1:8080/health
```

## Logs

```bash
bash scripts/observabilidade.sh
python scripts/dashboard.py
```

Execute o script do dashboard depois que o Kibana estiver disponível.
Acesse http://127.0.0.1:5601/app/dashboards#/view/devops-dashboard para consultar
logs, status HTTP e tempo médio de resposta. Se o IP do Elasticsearch mudar,
execute `observabilidade.sh` novamente. A configuração sem autenticação é destinada
a um laboratório local.
