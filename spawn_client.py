import sys
from client import Client
import time
if __name__ == "__main__":
    port_no = 10000
    try:
        port_no = "9898"#sys.argv[1]
        port_no = int(port_no)
        if(port_no<=0):
            raise ValueError
    except:
        print("Invalid arguments. Enter a number greater than zero.")
        sys.exit()

    my_client = Client(port_no)
    my_client.connect()
    print("exiting")
    time.sleep(3)
    sys.exit()