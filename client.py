import socket
import sys
import random
import uuid
import time
import re
from threading import Thread

class Client:
    def __init__(self, port_no):
        self.server_port = port_no
        self.client_id = uuid.uuid4()
    
    def is_number(self, string):
        try:
            int(string)
            return True
        except ValueError:
            return False

    def is_file(self, file_name):
        is_file_exist = ""
        try:
            with open(file_name, "r") as file:
                is_file_exist = True
        except:
            is_file_exist = False
        return is_file_exist    

    def perform_task(self, file_name, search_word):
        task_status = ""

        #if(not self.is_file(string)):
            #task_status = "Could not open the file : " + string                               #remove this cos of is_number
        #else:
        file = "/Users/gokkul/Desktop/olu/" + str(file_name)
        try:
            with open(file,"r") as f:
                f_text = f.read()
                print(f_text)
                #f_text = f_text.lower()
                out = "Performing the word search " + str(search_word) + " on " + str(file_name) + " file"
                print(out)
                #self.search_word = self.search_word.lower()
                if(re.search(search_word,f_text,re.IGNORECASE)):
                    out = search_word + " found in file '" + file_name +  "'" 
                    print(out)
                else:
                    print("No match found")                                                                           #document search
            task_status = "Completed task"
        except:
            task_status = "Could not complete task, there was an exception."
        return task_status

    def connect(self):

        print("Starting client:", self.client_id)
        #print("\n\n")
        # Create a TCP/IP socket
        # Connect the socket to the port where the server is listening
        server_address = ('localhost', self.server_port)
        print('connecting to %s port %s' % server_address)
        #print("\n\n")
        while(True):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(server_address)
                print("Connected to server successfully")
            except:
                print("Could not connect to server. Shutting down client.")
                sock.close()
                return
            try:
                print("Requesting filename from server")
                sock.sendall(str(self.client_id).encode('ascii'))
                sock.sendall("NEED_NEW_TASK".encode('ascii'))
                time.sleep(1)
                instruction_type = sock.recv(2).decode('ascii')
                instruction_type = int(instruction_type)
                print("Received instruction type: {0}".format(instruction_type))
                if(instruction_type == -1):
                    instruction = sock.recv(20).decode('ascii')  #filename <= 20 bytes
                    #print("Received instruction: ", instruction)
                    #print("\n\n")
                    print("Filename : {0}".format(instruction))
                    sock.sendall(str("SEND_SEARCH_WORD").encode('ascii'))
                    search_word = sock.recv(20).decode('ascii')
                    print("Search word : {0}".format(search_word))
                    task_status = self.perform_task(instruction,search_word)
                    print("Task Status:", task_status)
                    print("\n")
                if(instruction_type == -2):
                    print("Received SHUT_DOWN instruction")
                    break
            except:
                print("In except")
                sock.close()
            finally:
                sock.close()

        print("Shutting down Client", self.client_id)
        sock.close()

#my_client = Client(10000)
#my_client2 = Client(10000)
#Thread(target = my_client.connect()).start()
#Thread(target = my_client2.connect()).start()