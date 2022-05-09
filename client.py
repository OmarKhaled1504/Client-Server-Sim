import socket

if __name__ == "__main__":

    with open('commands.txt') as file:
        commands = file.readlines()
        commands = [command.rstrip() for command in commands]

    for command in commands:
        ip = command.split()[4].split(':')[0]
        port = int(command.split()[4].split(':')[1])
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((ip, port))

        filename = command.split()[1][1:]
        if command.split()[0] == "GET":
            server.sendall(bytes(command, "utf-8"))
        elif command.split()[0] == "POST":
            try:
                f = open(f"client files/{filename}", mode='r')
                data = f.read()
                contentLength = "\nContent-Length: " + str(len(data)) + "\n\n"
                request = command + contentLength + data
                server.sendall(bytes(request, "utf-8"))
            except IOError:
                print('file not found.')
        message = server.recv(4096)
        print(message.decode("utf-8"))
        server.close()
# TODO http 1.1 & bonus
