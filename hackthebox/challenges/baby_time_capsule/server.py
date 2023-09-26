from Crypto.Util.number import bytes_to_long, getPrime, long_to_bytes
import socketserver
import json

FLAG = b'HTB{this_is_very_very_long_because_then_it_is_harder_to_guess}'


class TimeCapsule():

    def __init__(self, msg):
        self.msg = msg
        self.bit_size = 1024
        self.e = 5

    def _get_new_pubkey(self):
        while True:
            p = getPrime(self.bit_size // 2)
            q = getPrime(self.bit_size // 2)
            n = p * q
            phi = (p - 1) * (q - 1)
            try:
                pow(self.e, -1, phi)
                break
            except ValueError:
                pass

        return n, self.e

    def get_new_time_capsule(self):
        n, e = self._get_new_pubkey()
        m_old = bytes_to_long(self.msg)
        #print(long_to_bytes(m_old))


        m = pow(m_old, e, n)

        if pow(m_old,e) < n:
            print(long_to_bytes(int(m**(1/e))))

        return {"time_capsule": f"{m:X}", "pubkey": [f"{n:X}", f"{e:X}"]}


def challenge(req):
    time_capsule = TimeCapsule(FLAG)
    while True:
        try:
            req.sendall(
                b'Welcome to Qubit Enterprises. Would you like your own time capsule? (Y/n) '
            )
            msg = req.recv(4096).decode().strip().upper()
            if msg == 'Y' or msg == 'YES':
                capsule = time_capsule.get_new_time_capsule()
                req.sendall(json.dumps(capsule).encode() + b'\n')
            elif msg == 'N' or msg == "NO":
                req.sendall(b'Thank you, take care\n')
                break
            else:
                req.sendall(b'I\'m sorry I don\'t understand\n')
        except:
            # Socket closed, bail
            return


class MyTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        req = self.request
        challenge(req)


class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def main():
    time_capsule = TimeCapsule(FLAG)
    time_capsule.get_new_time_capsule()
    time_capsule.get_new_time_capsule()
    time_capsule.get_new_time_capsule()
    time_capsule.get_new_time_capsule()
    time_capsule.get_new_time_capsule()
    time_capsule.get_new_time_capsule()
    time_capsule.get_new_time_capsule()
    time_capsule.get_new_time_capsule()
    time_capsule.get_new_time_capsule()
    time_capsule.get_new_time_capsule()


    # socketserver.TCPServer.allow_reuse_address = True
    # server = ThreadingTCPServer(("0.0.0.0", 1337), MyTCPRequestHandler)
    # server.serve_forever()


if __name__ == '__main__':
    main()
