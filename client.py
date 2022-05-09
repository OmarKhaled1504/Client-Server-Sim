import socket
from time import sleep

if __name__ == "__main__":

    with open('commands.txt') as file:
        commands = file.readlines()
        commands = [command.rstrip() for command in commands]

    for command in commands:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.settimeout(2)
        try:
            server.connect((command.split()[5].split(':')[0], int(command.split()[5].split(':')[1])))
        except IndexError:
            server.connect((command.split()[5].split(':')[0], 80))
        filename = command.split()[1][1:]
        if command.split()[0] == "GET":
            server.sendall(bytes(command, "utf-8"))
            while True:
                try:
                    message = server.recv(4096)
                    print(message.decode("utf-8"))
                except socket.timeout:
                    print("Server Timed Out\nConnection Closed")
                    break
        elif command.split()[0] == "POST":
            try:
                f = open(f"client files/{filename}", mode='r')
                data = f.read()
                contentLength = "\nContent-Length: " + str(len(data)) + "\n\n"
                request = command + contentLength + data
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
        sleep(10)
        server.close()
# TODO bonus
