"""Servidor local para as apresentações do curso."""
import http.server
import socketserver
import webbrowser
import os
import sys
import argparse
import glob
import json

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser(description="Servidor de apresentações")
parser.add_argument("--parte", choices=["1", "2"], default="1", help="Parte do curso (1 ou 2)")
parser.add_argument("--port", type=int, default=PORT, help="Porta do servidor")
args = parser.parse_args()

url_map = {
    "1": "/apresentacao/index.html",
    "2": "/apresentacao/parte2/index.html",
}

try:
    import build_apresentacao
    print("Construindo slides a partir dos arquivos individuais...")
    build_apresentacao.build_presentation('apresentacao')
    build_apresentacao.build_presentation('apresentacao/parte2')
except ImportError:
    pass

def get_latest_mtime():
    latest = 0
    # Monitor slides and templates (ignore built index.html files)
    for f in glob.glob('apresentacao/**/*.html', recursive=True):
        if 'index.html' not in f:
            mtime = os.path.getmtime(f)
            if mtime > latest:
                latest = mtime
    return latest

last_build_time = get_latest_mtime()

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
        
    def do_GET(self):
        # Intercept live-reload polling
        if self.path.startswith('/check-update'):
            global last_build_time
            current_mtime = get_latest_mtime()
            reload = False
            
            if current_mtime > last_build_time:
                print("\n[Live Reload] Modificação detectada! Reconstruindo slides...")
                try:
                    import build_apresentacao
                    build_apresentacao.build_presentation('apresentacao')
                    build_apresentacao.build_presentation('apresentacao/parte2')
                    # Update tracked time after build to avoid loops
                    last_build_time = get_latest_mtime()
                    reload = True
                except Exception as e:
                    print(f"Erro ao reconstruir: {e}")
                    
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            # Prevent caching of the polling request
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.end_headers()
            self.wfile.write(json.dumps({'reload': reload}).encode('utf-8'))
            return
            
        return super().do_GET()

    def log_message(self, format, *args):
        pass  # silencia logs

url = f"http://localhost:{args.port}{url_map[args.parte]}"
print(f"Iniciando apresentação Parte {args.parte}...")
print(f"Acesse: {url}")
print("Pressione Ctrl+C para encerrar.")

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", args.port), Handler) as httpd:
    webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
