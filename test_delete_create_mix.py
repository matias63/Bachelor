import socket
import threading

#TESTING delete, create x10, delete again
# EXPECTING: that responses come immidietly and that A is deleted adter threads have closed (mentioned in Back-End terminal)

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
        # NOTE: the print statements for deletion comes after the threads have lost connection due to the wait
    
    # while True:
    #     print("ended gracefully")

threads = []
# Delete A
thread = threading.Thread(target=send_request, args=("delete A",))
thread.start()
# Create A x10
for i in range(10):
    thread = threading.Thread(target=send_request, args=("create name:A, attack:6",))
    threads.append(thread)
    thread.start()
# Delete A
thread = threading.Thread(target=send_request, args=("delete A",))
threads.append(thread)
thread.start()
for thread in threads:
            thread.join()
