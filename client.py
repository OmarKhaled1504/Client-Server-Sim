import socket

if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 1234
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((ip, port))
    with open('commands.txt') as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
    for line in lines:
        server.send(bytes(line, "utf-8"))
    message = server.recv(1024)
    print(message.decode("utf-8"))
