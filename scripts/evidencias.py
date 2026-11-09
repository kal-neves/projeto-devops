"""salva saídas de comandos e captura sua visualização no navegador."""
import html
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright
out = Path('docs/evidencias')
out.mkdir(parents=True, exist_ok=True)
commands = {
    'pipeline': ['gh', 'run', 'view', '-R', 'kal-neves/projeto-devops', '--verbose'],
    'kubernetes': ['kubectl', '--context', 'kind-devops', '-n', 'devops', 'get', 'pods,svc', '-o', 'wide'],
}
with sync_playwright() as p:
    browser = p.chromium.launch()
    for name, command in commands.items():
        result = subprocess.run(command, check=True, capture_output=True, text=True).stdout
        (out / (name + '.txt')).write_text(result)
        document = '<meta charset="utf-8"><h2>Saída do comando - ' + name + '</h2><p>' + html.escape(' '.join(command)) + '</p><pre style="font-size:17px;white-space:pre-wrap">' + html.escape(result) + '</pre>'
        page = browser.new_page(viewport={'width': 1600, 'height': 1000})
        page.set_content(document)
        page.screenshot(path=str(out / (name + '.png')), full_page=True)
        page.close()
    browser.close()
