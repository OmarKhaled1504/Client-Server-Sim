import socket
from time import sleep

cache = {}


def compose(request_type, filename, host, port):
    return f'{request_type} /{filename} HTTP/1.1\r\nHOST: {host}:{port}'


if __name__ == "__main__":

    with open('commands.txt') as file:
        commands = file.readlines()
        commands = [command.rstrip() for command in commands]

    for command in commands:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.settimeout(2)
        ip = command.split()[2]
        try:
            server.connect((ip, int(command.split()[3][1:-1])))
            port = int(command.split()[3][1:-1])
        except IndexError:
            server.connect((command.split()[2], 80))
            port = 80
        filename = command.split()[1]
        if command.split()[0] == "GET":
            request = compose('GET', filename, ip, port)
            if filename in cache:
                with open(cache[f'{filename}'], 'r') as f:
                    print("file found in cache\n")
                    print(f.read())
            else:
                print('file not found in cache...\nrequesting from server...')
                server.sendall(bytes(request, "utf-8"))
                try:
                    message = server.recv(4096)
                    print(f'{message.decode("utf-8")}')
                    with open(f"server to client files/{command.split()[1][1:]}", 'w') as f:
                        f.write(message.decode("utf-8").split()[3])
                        cache.update({command.split()[1][1:]: f.name})
                except socket.timeout:
                    print("Server Timed Out\nConnection Closed")
                    break
        elif command.split()[0] == "POST":
            request = compose('POST', filename, ip, port)
            try:
                f = open(f"client files/{filename}", mode='r')
                data = f.read()
                contentLength = "\nContent-Length: " + str(len(data)) + "\n\n"
                request = request + contentLength + data
                server.sendall(bytes(request, "utf-8"))
            except IOError:
                print('file not found.')
            while True:
                try:
                    message = server.recv(4096)
                    print(message.decode("utf-8"))
                except socket.timeout:
                    print("Server Timed Out\nConnection Closed")
                    break
        sleep(6)
        server.close()
