from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler, HTTPServer
import time
import os
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json
import sqlite3


hostName = "localhost"
serverPort = 8080

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/FingerPrinter.html"
        try:
            f = open(os.curdir + self.path, "rb")
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
            return
        except IOError:
            self.send_error(404, "File not found")




    def do_GET(self):
        if self.path == "/":
            self.path = "/FingerPrinter.html"
        try:
            if self.path.endswith(".html"):
                f = open(os.curdir + self.path, "rb")
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
            elif self.path.endswith(".css"):
                f = open(os.curdir + self.path, "rb")
                self.send_response(200)
                self.send_header("Content-type", "text/css")
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
            elif self.path.endswith(".js"):
                f = open(os.curdir + self.path, "rb")
                self.send_response(200)
                self.send_header("Content-type", "application/javascript")
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return

            else:
                self.send_error(404, "File not found")
        except IOError:
            self.send_error(404, "File not found")



    def do_POST(self):
        if self.path == "/store-fingerprint":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = json.loads(post_data)
            fingerprint = post_data.get('fingerprint')
            name = post_data.get('name')
            store_fingerprint(fingerprint, name)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"message": "Fingerprint and name stored in database"}')
            return
        elif self.path == "/get-name":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = json.loads(post_data)
            fingerprint = post_data.get('fingerprint')
            conn = sqlite3.connect('fingerprints.db')
            cursor = conn.cursor()
            cursor.execute('SELECT name FROM fingerprints WHERE fingerprint = ?', (fingerprint,))
            result = cursor.fetchone()
            if result:
                name = result[0] or "Anonymous"
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"name": name}).encode())
                conn.close()
                return
            else:
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"error": "Fingerprint not found in database"}')
                conn.close()
                return
        else:
            self.send_error(404, "File not found")


def store_fingerprint(fingerprint, name):
    conn = sqlite3.connect('fingerprints.db')
    cursor = conn.cursor()

    try:
        # Vérifier si le hash existe déjà dans la base de données
        cursor.execute('SELECT name FROM fingerprints WHERE fingerprint = ?', (fingerprint,))
        result = cursor.fetchone()
        if result:
            existing_name = result[0]
            return existing_name or "Anonymous"
        else:
            # Ajouter le hash à la base de données avec le nom donné en paramètre ou "Anonymous" si name est vide
            name_to_insert = name if name else "Anonymous"
            cursor.execute('INSERT INTO fingerprints (fingerprint, name) VALUES (?, ?)', (fingerprint, name_to_insert))
            conn.commit()
            print('Hash added to database')
            return name_to_insert
    except sqlite3.Error as e:
        print("SQL error:", e)
        return None
    finally:
        conn.close()



class MyEventHandler(FileSystemEventHandler):
    def __init__(self, server):
        self.server = server

    def on_modified(self, event):
        if event.is_directory or not event.src_path.endswith(".py"):
            return
        print(f"{event.src_path} has been modified, restarting server...")
        self.server.shutdown()

def main():
    handler = MyHandler
    server = ThreadingHTTPServer(("0.0.0.0", 8080), handler)
    event_handler = MyEventHandler(server)
    observer = Observer()
    observer.schedule(event_handler, sys.path[0], recursive=False)
    observer.start()

    print("Server started on http://localhost:8080")
    server.serve_forever()
    observer.stop()
    print("Server stopped.")
    
if __name__ == "__main__":
    main()
