import socket

class PyMaxDB:

    def __init__(self, database, host, port=6756, username=None, password=None):
        self.db = database
        self.port = port
        self.username = username
        self.password = password
        self.host = host
    def query(self, query):
        sock = socket.socket()
        sock.connect((self.host, self.port))
        sock.send(query+" "+self.db+" "+self.username+" "+self.password)
        return sock.recv(1024)
        sock.close()
