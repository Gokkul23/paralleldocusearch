import sys
from server import Server

def server_launch_util(number_of_tasks,file_name,search_word, port_no):
    my_server = Server(number_of_tasks,file_name,search_word,port_no)
    my_server.launch()

if __name__ == "__main__":
    try:
        number_of_tasks = sys.argv[1]
        number_of_tasks = int(number_of_tasks)
        if(number_of_tasks<=0):
            raise ValueError
        file_name = []
        print("Enter ",number_of_tasks, " filename(s)")
        for i in range(number_of_tasks):
            x = input("Enter filename {0} : ".format(i+1))
            file_name.append(x)
        search_word = ""
        print("\n")
        search_word = input("Search the word : ")
        if(len(search_word) == 0):
            print("Not valid search word")
            raise ValueError    
        if(len(file_name)==0):
            raise ValueError
        port_no = "9898"#sys.argv[2]
        port_no = int(port_no)
        if(port_no<=0):
            raise ValueError
    except:
        print("Invalid arguments. arg1: number of tasks, arg2: port no. Both should have values greater than zero")
        sys.exit()

    server_launch_util(number_of_tasks,file_name,search_word, port_no)