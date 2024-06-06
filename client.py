import socket
# code borrowed by https://www.datacamp.com/tutorial/a-complete-guide-to-socket-programming-in-python

def run_client():
    # create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "127.0.0.1"  # replace with the server's IP address
    server_port = 8000  # replace with the server's port number
    # establish connection with server
    client.connect((server_ip, server_port))

    try:
        while True:
            # get input message from user and send it to the server
            msg = input("Enter message: ")
            client.send(msg.encode("utf-8")[:1024])
            if msg.lower() == "shutdown":
                client.close()
                exit(0)
            # receive message from the server
            
            response = client.recv(1024)    
            response = response.decode("utf-8")
            print(f"Received: {response}")
            # if server sent us "closed" in the payload, we break out of
            # the loop and close our socket
            if response.lower() == "closed":
                break
            
            if  response.isdigit():
                # print("receiving img")
                for i in range(1,int(response)+1):
                    receive_image(client, f'received_image_{i}.jpg')
                print("image received")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()
        print("Connection to server closed")

def receive_image(sock, image_path, buffer_size=4096):
        with open(image_path, 'wb') as f:
            total_received = 0
            while True:
                data = sock.recv(buffer_size)
                total_received += len(data)
                # print(f"Received {len(data)} bytes. Total received: {total_received} bytes")
                f.write(data)
                if len(data)< 4096:     # bug if last package is the same length as the rest of the packages - i cant fix. ive been tryingf´for days (could send an etra last byte before break to fix-ish?)
                    # print("End of file")
                    break
    
            


run_client()
