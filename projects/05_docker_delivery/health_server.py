from http.server import HTTPServer,BaseHTTPRequestHandler
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  if self.path!='/health':self.send_error(404);return
  body=b'{"status":"ok","synthetic":true}'
  self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
if __name__=='__main__':HTTPServer(('0.0.0.0',8000),Handler).serve_forever()
