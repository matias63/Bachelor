import socket
import threading
import current
import time
import re
import os
import json
# code borrowed by https://www.datacamp.com/tutorial/a-complete-guide-to-socket-programming-in-python

# Lock and locking list for concurrency control 
lock = threading.Lock()
param_locks = {}

# nr_file = current.next_card_id

# handle client requests
def handle_client(client_socket, addr,server):
    try:
        while True:
            # receive and print client messages
            request = client_socket.recv(1024).decode("utf-8")
            
            # let a client close the connection gracefully
            if request.lower() == "close":
                client_socket.send("closed".encode("utf-8"))
                break

            # idea by Hannu https://stackoverflow.com/questions/44387712/python-sockets-how-to-shut-down-the-server
            # close Server
            if request.lower() == "shutdown":
                server.close()
                exit(0)
            print(f"Received: {request}")
            
            # Execute request and respond
            response,card = execute_command(request)
            client_socket.send(response.encode("utf-8"))
            print(f"Sending response: {response}")
            time.sleep(1)
            
            # Send images
            try:
                if  int(response):
                    # print("images sending")
                    for i in card[1:]:
                        send_image(client_socket,i)
                    print("images send")
            except:
                pass
            # print(current.cache_len())
    except Exception as e:
        print(f"Error when handling client: {e}")
    finally:
        client_socket.close()
        print(f"Connection to client ({addr[0]}:{addr[1]}) closed")

# One time use to create the database setup
def load_index():
    script_dir = os.path.dirname(__file__)
    path = f"search_index.json"
    abs_file_path = os.path.join(script_dir, path)
    with open(abs_file_path, 'r', encoding='utf-8', errors='ignore') as file:
        data = json.load(file)
    return data

# check if a param exists in index
def find_index(data,param):
    if param.title() in data:
        return True
    return False

# find the name of a card being created
def create_name_finder(param):
    n = re.search(r'name:([^,\s]+)',param)
    n = n.group(1)
    print("create_name_finder:" ,n)
    return str(n)

# updates the database index schema
def update_index(cached_index):
    script_dir = os.path.dirname(__file__)
    path = f"search_index.json"
    abs_file_path = os.path.join(script_dir, path)
    with open(abs_file_path, 'w', encoding='utf-8', errors='ignore') as file:
        file.write(json.dumps(cached_index))

# Timer to update index based on the program updates - unused
def timer(data):
    start_time = time.time()
    if time.time() - start_time >=10:
        print("yes")
        update_index(data)
        start_time = time.time()


# Execute client commands
def execute_command(msg):
    msg = msg.lower()
    # Split mesage into "msg type" and "parameter"
    if len(msg.split(" ",1)) == 2:
        msg,param = msg.split(" ",1)

    if param is None:
        return "No parameter provided", []
    else:
        response,card = perform(msg,param)
        return response,card

def perform(msg,param):
    try:

        # Pattern match card names
        if msg == "search":
            # NOTE: Has No Read-Lock, but is protected by the rules of execute_command: create, delete and rules in current.search_id
            # card = current.thread_search(param)
            local_cache = current.thread_search(param)
            card = current.image_processing(local_cache,param)
            if card == "error":
                return f"{param} not available",[]
            return str(len(card)-1),card
        
        elif msg == "test1_old":
            # NOTE: Has No Read-Lock, but is protected by the rules of execute_command: create, delete and rules in current.search_id
            local_cache = current.thread_search_before_indexing(param)
            # card = current.image_processing(local_cache,param)
            if local_cache == "error":
                return f"{param} not available",[]
            return  "0",[]
        
        elif msg == "test2_old":
            # NOTE: Has No Read-Lock, but is protected by the rules of execute_command: create, delete and rules in current.search_id
            local_cache = current.thread_search_before_indexing(param)
            card = current.image_processing(local_cache,param)
            if card == "error":
                return f"{param} not available",[]
            return str(len(card)-1),card

        # TEST for search speed
        elif msg == "test1":
            # NOTE: Has No Read-Lock, but is protected by the rules of execute_command: create, delete and rules in current.search_id
            local_cache = current.thread_search(param)
            # card = current.image_processing(local_cache,param)
            if local_cache == "error":
                return f"{param} not available",[]
            return "0",[]
        
        # TEST for search and image_processing speed
        elif msg == "test2":
            local_cache = current.thread_search(param)
            card = current.image_processing(local_cache,param)
            if card == "error":
                return f"{param} not available",[]
            return str(len(card)-1),card
        
        else:
            # Fit a responsible thread lock name for creating cards
            if msg == "create":
                n = param
                param = create_name_finder(param)
            
            # Thread lock actions
            # NOTE: multi-lock system - 1 lock locks this section. This sections provides a second lock based on the param you want to modify.
            param = param.title()
            while True:
                lock.acquire(blocking=True) 
                try:
                    if param not in param_locks:
                            param_locks[param] = threading.Lock()
                    param_locks[param].acquire()
                    print("     Added lock for", param)
                    break
                finally:
                    print("Release main lock")
                    lock.release()
                
           
            # View param lock states
            # print("                                         PARAM_LOCKS",param_locks)

            #delete a card
            if msg == "delete":
                param_exists = find_index(data,param)
                if param_exists:
                    try:
                            del data[param.title()] # remove card from search index, so it CAN'T BE READ anymore
                            # NOTE: Concurrency control for deleting an entry from the DBMS (SAFETY: READ-LOCK is unnecessary)
                            # NOTE: Deletes the entry in the DBMS if CREATE has not inserted the param in search_index.py 
                            thread = threading.Thread(target=delete_cleanup, args=(param,))
                            thread.start()
                            return param+" has been deleted",[]
                    except:
                            return f"error deleting {param}",[]
                    finally:
                            print("     releasing lock for ",param)
                            param_locks[param].release()
                else:
                    print("     releasing lock for ",param)
                    param_locks[param].release()
                    return param +" doesnt exist",[]           # has to send a card for client to work
            
            #create a card
            # NOTE: search safety placed in current.search_id() - if card is in search_index, but cant find meta_data, try again (card must be updating)
            elif msg == "create":
                try:
                        param = current.create(n)
                        if param not in data:
                            data[param] = ""
                            return param+" has been created",[]
                        return param+" has been updated",[]
                except:
                        return f"error creating {param}",[]
                finally:
                        print("     releasing lock for ",param)
                        param_locks[param].release()

            # if it really breaks down
            return f"{param} not available",[]
    except Exception as e:
        return f"Error when handling client request: {e}",[]
    # update card_index schema used in database 
    finally: update_index(data)

# Send images
def send_image(sock, image_path, buffer_size=4096):
    with open(image_path, 'rb') as f:
        while True:
            data = f.read(buffer_size)
            if not data:
                # print("End of file")
                break
            sock.sendall(data)
            # print(f"Sent {len(data)} bytes")


def delete_cleanup(param):
    # time.sleep(60) #deletion delay such that all current searches for the card can still find the card.
    time.sleep(3) #deletion delay sfor testing
    lock.acquire(blocking=True) 
    try:
        if param not in data:
            param_locks[param].acquire()
            print("     Added DELETE LOCK for", param)
            deleted_item = current.delete(param)
            print(deleted_item)
            print("     releasing lock for ",param)
            param_locks[param].release()
        else:
             print(param +" Doesn't exist")
    finally:
        print("Release main lock")
        lock.release()


# Start Back-End / Server
def run_server():
    server_ip = "127.0.0.1" 
    port = 8000 

    # cache the index library
    global data
    data = load_index()

    try:
        # Server: create a socket and listen 
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((server_ip, port))
        server.listen()
        print(f"Listening on {server_ip}:{port}")

        while True:
            # accept a client connection
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")
            # start a new thread to handle the client
            thread = threading.Thread(target=handle_client, args=(client_socket, addr,server,))
            thread.start()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.close()


run_server()