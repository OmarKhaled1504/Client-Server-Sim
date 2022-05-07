import socket


def parse(request):
    if request.split()[0] == 'GET':
        filename = request.split()[1]
        return "get", filename
    elif request.split()[0] == 'POST':
        return "post"


if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 1234

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(5)

    while True:
        client, address = server.accept()
        print(f"connection established - {address[0]}:{address[1]}")
        request = client.recv(1024)
        request = request.decode("utf-8")
        request_type, filename = parse(request)
        if request_type == "get":
            try:
                f = open(f"server files/{filename}", mode='r')
                message = f.read()
            except IOError:
                message = "HTTP/1.0 404 Not Found\r\n"
            client.send(bytes(message, "utf-8"))
        client.close()
