import socket
import threading

# Socket creation, connecting, sending and receiving from/to back end
def send_request(msg):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("127.0.0.1", 8000))
        client_socket.send(msg.encode("utf-8"))
        response = client_socket.recv(1024).decode("utf-8")
        print(f"Response: {response}           TEST")
    except Exception as e:
        print(f"Error: {e}") 
    
        # NOTE: The test will result in alot of error messages, since each thread will be forcefully shut down
        # NOTE: The test also results in the Back-end receiving an empty mesage. 
        # NOTE: Therefore inserting the outcommented infinity loop makes it error free, but the server needs to be killed manually
        # NOTE: Testing have been done with both this option on and off to test edge case of the threads program ending with unsent message
        
    # while True:
    #     print("ended gracefully")


        




threads = []
# Send different threads to test if multiple parameters can be deleted at the same time:
thread = threading.Thread(target=send_request, args=("delete spirits",))
thread = threading.Thread(target=send_request, args=("delete Fury Sliver",))
thread.start()
for i in range(500):
    thread = threading.Thread(target=send_request, args=("delete A",))
    threads.append(thread)
    thread.start()
# Retring to delete a deleted param should result in the message: "Spirits not available"
thread = threading.Thread(target=send_request, args=("delete spirits",))
thread.start()

# for thread in threads:
#     thread.join()


# threads =[]
# for i in range(5):
#     # Create a new thread and pass the thread function and its arguments
#     thread = threading.Thread(target=send_request, args=(f"delete param{i}",))
    
#     # Start the thread
#     thread.start()
    
#     # Append the thread object to the list
#     threads.append(thread)


