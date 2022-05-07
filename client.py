import socket

if __name__ == "__main__":

    ip = "127.0.0.1"
    port = 1234
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((ip, port))
    with open('commands.txt') as file:
        commands = file.readlines()
        commands = [command.rstrip() for command in commands]
    for command in commands:
        command = command + f"\nHOST: {ip}"
        filename = command.split()[1]
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
