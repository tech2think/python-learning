"""Servidor local para as apresentações do curso."""
import http.server
import socketserver
import webbrowser
import os
import sys
import argparse

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

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    def log_message(self, format, *args):
        pass  # silencia logs

url = f"http://localhost:{args.port}{url_map[args.parte]}"
print(f"Iniciando apresentação Parte {args.parte}...")
print(f"Acesse: {url}")
print("Pressione Ctrl+C para encerrar.")

with socketserver.TCPServer(("", args.port), Handler) as httpd:
    webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
