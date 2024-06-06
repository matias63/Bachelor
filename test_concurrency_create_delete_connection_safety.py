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
        
    while True:
        print("ended gracefully")


# Delete A
thread = threading.Thread(target=send_request, args=("delete A",))
thread.start()
# Create A x10
for i in range(100):
    thread = threading.Thread(target=send_request, args=("create name:A, attack:6",))
    thread.start()
