import socket
import threading
from _thread import *

print_lock = threading.Lock()


def threaded(client):
    while True:
        try:
            request = client.recv(4096)
            request = str(request)[2:-1]
            if not request:
                print('Connection closed')
                print_lock.release()
                break
        except socket.timeout:
            print_lock.release()
            client.close()
            print("Operation Timed Out\nConnection Closed")
            break

        request_type, filename = parse(request)
        reply = "HTTP/1.0 200 OK\r\n"
        if request_type == "get":
            if filename.split(".")[1] == "txt":
                try:
                    f = open(f"server files/{filename}", mode='r')
                    reply = reply + f.read() + "\r\n"
                except IOError:
                    reply = "HTTP/1.0 404 Not Found\r\n"
                client.sendall(bytes(reply, "utf-8"))
            elif filename.split(".")[1] == "png":
                f = open(f"server files/{filename}", mode='rb')
                img = f.read(1024)
                while img:
                    client.send(img)
                    img = f.read(1024)
        elif request_type == "post":
            if filename.split(".")[1] == "txt":
                data = request.split()[-1]
                print(f"data: {data}")
                with open(f"client to server files/{request.split()[1][1:]}", 'w') as f:
                    f.write(data)
                client.sendall(bytes(reply, "utf-8"))
            elif filename.split(".")[1] == "png":
                with open(f"client to server files/{filename}", 'wb') as f:
                    while True:
                        try:
                            message = client.recv(4096)
                        except socket.timeout:
                            break
                        if not message:
                            break
                        else:
                            f.write(message)
                client.sendall(bytes(reply, "utf-8"))


def parse(request):
    try:
        if request.split()[0] == 'GET':
            filename = request.split()[1][1:]
            return "get", filename
        elif request.split()[0] == 'POST':
            filename = request.split()[1][1:]
            return "post", filename
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
        client.settimeout(5)
        print_lock.acquire()
        start_new_thread(threaded, (client,))
