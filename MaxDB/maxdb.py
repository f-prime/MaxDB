#!/usr/bin/python
import socket, sys, threading

class MaxDB:
    def __init__(self):
        try:
            self.port = int(sys.argv[1])
        except IndexError:
            self.port = 6756
        self.queries = {

                "GET":self.get,
                "PUT":self.put,
                "CREATE":self.create,
                "DEL":self.delete,
                }
        self.users = {

                "root":"461408"

                }
    def main_loop(self):
        print "MaxDB is running on port "+str(self.port)
        sock = socket.socket()
        sock.bind(('', self.port))
        sock.listen(5)
        while True:
            obj, conn = sock.accept()
            data = obj.recv(1024)
            print conn[0], data
            data = data.split()
            username = data[len(data)-2]
            password = data[len(data)-1]
            data.remove(username)
            data.remove(password)
            data = ' '.join(data)
            if username in self.users:
                if self.users[username] == password:
                    for query in self.queries:
                        if data.startswith(query):
                            threading.Thread(target=self.queries[query], args=(data, obj)).start()
                            break
                else:
                    obj.send("MaxDB Error: You don't have access to this database.")
                    obj.close()
    def get(self, query, obj):
        #GET members username='username' password='password' database
        try:
            query = query.split()
            query.remove("GET")
            table = query[0]
            query.remove(table)
            database = query[len(query)-1]
            query.remove(database)
        except:
            obj.send("MaxDB Error: There is an error in your MaxDB query.")
        try:
            lines = []
            with open(database+".maxdb", 'rb') as file:
                for line in file.readlines():
                    line = line.rstrip("\n")
                    if line.startswith(table):
                        check = ' '.join(query)
                        if check in line:
                            line = line.split(":")[1]
                            lines.append(line)
            obj.send(str(lines))
        except:
            obj.send("MaxDB Error: Database doesn't exist.")
        obj.close()

    def put(self, query, obj):
        try:
            query = query.split()
            query.remove("PUT")
            table = query[0]
            query.remove(table)
            database = query[len(query)-1]
            query.remove(database)
            query = " ".join(query)
        except:
            obj.send("MaxDB Error: There is an error in your MaxDB query.")
        try:
            with open(database+".maxdb", 'a') as file:
                file.write(table+":"+query+"\n")
        except Exception, error:
            print error
            obj.send("MaxDB Error: Database doesn't exist.")
        obj.close()

    def create(self, query, obj):
        try:
            query = query.split()
        except:
            obj.send("MaxDB Error: There is an error in your MaxDB query.")
        with open(query[1]+".maxdb", 'wb') as file:
            file.write('')
        obj.close()

    def delete(self, query, obj):
        try:
            query = query.split()
            query.remove("DEL")
            table = query[0]
            query.remove(table)
            database = query[len(query)-1]
            query.remove(database)
            query = " ".join(query)
        except:
            obj.send("MaxDB Error: There is an error in your MaxDB query.")
        try:
            read = open(database+".maxdb", 'rb').read()
            done = read.replace(table+":"+query, '')
            write = open(database+".maxdb", 'wb')
            write.write(done)
            write.close()
        except Exception, error:
            print error
            obj.send("MaxDB Error: Database doesn't exist.")
        obj.close()
if __name__ == "__main__":
    try:
        MaxDB().main_loop()
    except KeyboardInterrupt:
        exit()
