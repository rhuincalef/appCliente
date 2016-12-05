from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer import ThreadingMixIn
import threading
import argparse
import re
import cgi
from json import JSONEncoder

# Comando para iniciar el servidor
# python simplewebserver.py


# GET test -->
# POST test -->
# https://mafayyaz.wordpress.com/2013/02/08/writing-simple-http-server-in-python-with-rest-and-json/
class LocalData(object):
  records = {}


class FallasInformadas(object):
  fallas = {
  "1":{ "id": 1,
      "calle": "Belgrano",
      "altura": 200},
  "2":{ "id": 2,
      "calle": "Irigoyen",
      "altura": 200},
  "3":{ "id": 3,
      "calle": "Ameguino",
      "altura": 200},
  "4":{ "id": 4,
      "calle": "Pellegrini",
      "altura": 200},
  "5":{ "id": 5,
      "calle": "9 de Julio",
      "altura": 200},
  "6":{ "id": 6,
      "calle": "Aedo",
      "altura": 200},
  "7":{ "id": 7,
      "calle": "Callao",
      "altura": 200}
  }


  
 
class HTTPRequestHandler(BaseHTTPRequestHandler):
  def do_POST(self):
    if None != re.search('/api/v1/addrecord/*', self.path):
      ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
      if ctype == 'application/json':
        length = int(self.headers.getheader('content-length'))
        data = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
        recordID = self.path.split('/')[-1]
        LocalData.records[recordID] = data
        print "record %s is added successfully" % recordID
      else:
        data = {}
      self.send_response(200)
      self.end_headers()
    else:
      self.send_response(403)
      self.send_header('Content-Type', 'application/json')
      self.end_headers()
    return
 
  def do_GET(self):
    if None != re.search('/api/falla/get/informados/*', self.path):
      self.send_response(200)
      self.send_header('Content-Type', 'application/json')
      self.end_headers()
      json_respuesta = JSONEncoder().encode(FallasInformadas.fallas)
      self.wfile.write(json_respuesta)
      # recordID = self.path.split('/')[-1]
      # if LocalData.records.has_key(recordID):
      #   self.send_response(200)
      #   self.send_header('Content-Type', 'application/json')
      #   self.end_headers()
      #   self.wfile.write(LocalData.records[recordID])
      # else:
      #   self.send_response(400, 'Bad Request: record does not exist')
      #   self.send_header('Content-Type', 'application/json')
      #   self.end_headers()
    else:
      self.send_response(403)
      self.send_header('Content-Type', 'application/json')
      self.end_headers()
    return
 
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
  allow_reuse_address = True
 
  def shutdown(self):
    self.socket.close()
    HTTPServer.shutdown(self)
 
class SimpleHttpServer():
  def __init__(self, ip, port):
    self.server = ThreadedHTTPServer((ip,port), HTTPRequestHandler)
 
  def start(self):
    self.server_thread = threading.Thread(target=self.server.serve_forever)
    self.server_thread.daemon = True
    self.server_thread.start()
 
  def waitForThread(self):
    self.server_thread.join()
 
  def addRecord(self, recordID, jsonEncodedRecord):
    LocalData.records[recordID] = jsonEncodedRecord
 
  def stop(self):
    self.server.shutdown()
    self.waitForThread()
 
if __name__=='__main__':
  # parser = argparse.ArgumentParser(description='HTTP Server')
  # parser.add_argument('port', type=int, help='Listening port for HTTP Server')
  # parser.add_argument('ip', help='HTTP Server IP')
  # args = parser.parse_args()
  
  # 
  # server = SimpleHttpServer(args.ip, args.port)
  server = SimpleHttpServer("127.0.0.1", 8080)
  print 'HTTP Server Running...........'
  server.start()
  server.waitForThread()