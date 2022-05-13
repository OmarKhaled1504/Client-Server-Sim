import socket
from time import sleep
from PIL import Image

cache = {}


def compose(request_type, filename, host, port):
    return f'{request_type} /{filename} HTTP/1.1\r\nHOST: {host}:{port}\r\n'


if __name__ == "__main__":
    commands_file = input("Enter Commands File Name With Extension: ")
    try:
        with open(commands_file) as file:
            commands = file.readlines()
            commands = [command.rstrip() for command in commands]
    except FileNotFoundError:
        print("File Not Found!")
        exit()
    for command in commands:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
                    if filename.split(".")[1] == "txt":
                        print(f.read())
                    elif filename.split(".")[1] == "png":
                        image = Image.open(cache[f'{filename}'])
                        image.show()
            else:
                print('file not found in cache...\nrequesting from server...')
                server.sendall(bytes(request, "utf-8"))

                if filename.split(".")[1] == "txt":
                    message = server.recv(4096)
                    print(f'{message.decode("utf-8")}')
                    with open(f"server to client files/{filename}", 'w') as f:
                        f.write(message.decode("utf-8").split()[3])
                        cache.update({filename: f.name})
                elif filename.split(".")[1] == "png":
                    with open(f"server to client files/{filename}", 'wb') as f:
                        cache.update({filename: f.name})
                        while True:
                            message = server.recv(4096)
                            if not message:
                                break
                            else:
                                f.write(message)
                    print("image received successfully")
                    image = Image.open(cache[f'{filename}'])
                    image.show()
        elif command.split()[0] == "POST":
            request = compose('POST', filename, ip, port)
            if filename.split(".")[1] == "txt":
                try:
                    f = open(f"client files/{filename}", mode='r')
                    data = f.read()
                    contentLength = "\nContent-Length: " + str(len(data)) + "\n\n"
                    request = request + contentLength + data
                    server.sendall(bytes(request, "utf-8"))
                except IOError:
                    print('file not found.')
            elif filename.split(".")[1] == "png":
                try:
                    f = open(f"client files/{filename}", mode='rb')
                except IOError:
                    print(f'file ({filename}) not found!')
                    continue
                server.send(bytes(request, 'utf-8'))
                img = f.read(1024)
                while img:
                    server.send(img)
                    img = f.read(1024)
            message = server.recv(4096)
            print(message.decode("utf-8"))

        server.close()
