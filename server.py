import socket
import sys
import random
from uuid import UUID
class Server:

    def __init__(self, no_of_tasks,file_name,search_word, port_no):
        self.port = port_no
        self.tasks = []
        self.search_word = search_word
        self.client_task_dictionary = {}
        self.found_clients = False
        self.client_list = []
        for i in range(0, no_of_tasks):
            self.tasks.append(file_name[i])

    def parse_guid(self, guid_string, version = 4):
        try:
            uuid_obj = UUID(guid_string, version=version)
            return uuid_obj
        except:
            print("Invalid GUID:",guid_string)
            return False

    def all_clients_are_free(self):
        all_clients_free = True
        for client in self.client_task_dictionary:
            if(self.client_task_dictionary[client] != -1):
                all_clients_free = False
                break
        return all_clients_free

    def get_new_connection_GUID(self, sock):
        connection, client_id = sock.accept()
        guid_message = connection.recv(36).decode('ascii')
        print("Received GUID of client:", guid_message)
        guid = self.parse_guid(guid_message)
        return guid, connection

    def send_random_task(self, guid, connection):
        connection.sendall(str(-1).encode('ascii'))
        #next_i= random.randint(0,len(self.tasks) - 1)
        load = self.tasks[0]                                                            #give file name
        print("Sending task ", load)
        connection.sendall(str(load).encode('ascii'))
        #search = self.search_word
       ## print("Sending search word ", search_word)
       # connection.sendall(str(search).encode('ascii'))
        self.client_task_dictionary[guid] = load
        self.tasks.pop(0)

    def send_search(self,guid,connection):
        search = self.search_word
        print("Sending search word ", self.search_word)
        connection.sendall(str(search).encode('ascii'))

    def launch(self):
        #server socket setup and binding
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_address = ('localhost', self.port)
        print ('starting up on %s port %s' % server_address)
        sock.bind(server_address)

        sock.listen(1)

        while(len(self.tasks)>0):
            guid,connection = self.get_new_connection_GUID(sock)
            if(not guid):
                connection.close()
                continue
            message = connection.recv(13).decode('ascii')
            if(message == "NEED_NEW_TASK"):
                self.send_random_task(guid,connection)
            message = connection.recv(16).decode('ascii')
            if(message == "SEND_SEARCH_WORD"):    
                self.send_search(guid,connection)
            connection.close()

        while(not self.all_clients_are_free()):
            guid,connection = self.get_new_connection_GUID(sock)
            if(not guid):
                connection.close()
                continue

            message = connection.recv(13).decode('ascii')
            if(message == "NEED_NEW_TASK"):
                print("Sending SHUT_DOWN signal")
                connection.sendall(str(-2).encode('ascii'))
                self.client_task_dictionary[guid] = -1
            connection.close()

        print("Completed all tasks using: ",len(self.client_task_dictionary)," clients")
        print("Shutting down server...")
        sock.close()