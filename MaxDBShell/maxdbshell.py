#!/usr/bin/python
import socket, sys, pymaxdb

class MaxDBShell:
    def __init__(self):
        self.host = sys.argv[1]
        self.port = int(sys.argv[2])
        self.username = sys.argv[3]
        self.password = sys.argv[4]
        self.database = sys.argv[5]
        self.cur = pymaxdb.PyMaxDB(host=self.host, port=self.port, database=self.database, username=self.username, password=self.password)
    def main_loop(self):
        while True:
            query = raw_input("MaxDB> ")
            if query == "exit":
                print "Bye"
                exit()
            print self.cur.query(query)
            
if __name__ == "__main__":
    MaxDBShell().main_loop()
