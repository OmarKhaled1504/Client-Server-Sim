import socket
import threading
from _thread import *

print_lock = threading.Lock()


def threaded(client):
    while True:
        try:
            request = client.recv(4096)
            if not request:
                print('Connection closed')
                print_lock.release()
                break
            print(request)
        except socket.timeout:
            print_lock.release()
            client.close()
            print("Operation Timed Out\nConnection Closed")
            break
        request = request.decode("utf-8")

        request_type, filename = parse(request)
        message = "HTTP/1.0 200 OK\r\n"
        if request_type == "get" and filename.split(".")[1] == "txt":
            try:
                f = open(f"server files/{filename}", mode='r')
                message = message + f.read() + "\r\n"
            except IOError:
                message = "HTTP/1.0 404 Not Found\r\n"
            client.sendall(bytes(message, "utf-8"))
        elif request_type == "post":
            data = request.split()[-1]
            print(f"data: {data}")
            with open(f"client to server files/{request.split()[1][1:]}", 'w') as f:
                f.write(data)
            client.sendall(bytes(message, "utf-8"))
        elif request_type == "get" and filename.split(".")[1] == "png":
            f = open(f"server files/{filename}", mode='rb')
            l = f.read(1024)
            while l:
                client.send(l)
                l = f.read(1024)

        #elif request_type == "post" and filename.split(".")[1] == "png":
    client.close()


def parse(request):
    try:
        if request.split()[0] == 'GET':
            filename = request.split()[1][1:]
            return "get", filename
        elif request.split()[0] == 'POST':
            return "post", None
    except IndexError:
        return None, None


if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 80
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    print("Server started")
    print("socket bound to port", port)
    print("Waiting for client request..")
    server.listen()
    while True:
        client, address = server.accept()
        client.settimeout(10)
        print_lock.acquire()
        start_new_thread(threaded, (client,))
