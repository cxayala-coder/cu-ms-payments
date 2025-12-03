#!/usr/bin/env python3
"""
Servidor HTTP simple que responde Hola Mundo
"""
import http.server
import socketserver
import sys
from datetime import datetime

PORT = 3000

class HolaMundoHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Solicitud GET recibida", file=sys.stdout)
        print(f"[{timestamp}] Path: {self.path}", file=sys.stdout)
                
        # Endpoints de health/startup
        if self.path in ('/startup', '/liveness', '/readiness'):
            # Log cada vez que se llama al endpoint
            print(f"se llamo a endpoint {self.path}")
            sys.stdout.flush()            
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'OK')
            return

        # Comportamiento por defecto
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(b'<h1>Hola Mundo</h1>')
    
    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format%args}")
        sys.stdout.flush()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {self.address_string()} - {format%args}", file=sys.stdout)
        sys.stdout.flush()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), HolaMundoHandler) as httpd:
        print(f"Servidor corriendo en puerto {PORT}")
        print("Presiona Ctrl+C para detener")
        httpd.serve_forever()