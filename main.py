from os import abort, fork

from config import PORT

from socket import socket, getaddrinfo
from socket import AF_INET, SOCK_STREAM, IPPROTO_TCP, AI_ADDRCONFIG, AI_PASSIVE, SOL_SOCKET, SO_REUSEADDR


def handle_request(tcpSocket, connection):
    tcpSocket.close()

    while True:
        message = connection.recv(1024)

        if message is None:
            break

        connection.send(
            'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode())
        connection.send("""
            <html>
            <body>
            <h1>Hello World</h1> this is my server!
            </body>
            </html>
        """.encode())  # Use triple-quote string.

    connection.close()
    print('Connection closed')
    exit()


def connect(tcpSocket):
    (connection, client) = tcpSocket.accept()
    print('Server is connected with', client)

    return connection


def listen(tcpSocket):
    try:
        tcpSocket.listen(0)

    except:
        print('Failed to initialize socket')
        abort()

    return


def bind(tcpSocket, port):
    try:
        tcpSocket.bind(('', port))

    except:
        print('Failed to bind socket')
        abort()

    return


def create_socket(host_address):
    tcpSocket = socket(host_address[0][0], host_address[0][1])

    if tcpSocket is None:
        print('Failed to create socket')
        abort()

    return tcpSocket


def get_host_address(port):
    try:
        address = getaddrinfo(
            None,
            port,
            AF_INET,
            SOCK_STREAM,
            IPPROTO_TCP,
            AI_ADDRCONFIG | AI_PASSIVE
        )

    except:
        print("Failed to get host address")
        abort()

    return address


def init():
    host_address = get_host_address(PORT)
    tcpSocket = create_socket(host_address)
    tcpSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    bind(tcpSocket, PORT)
    listen(tcpSocket)

    print('Server initialized on port', PORT)

    while True:
        connection = connect(tcpSocket)

        if connection == -1:
            continue

        pid = fork()

        if pid == 0:
            handle_request(tcpSocket, connection)

        else:
            connection.close()


if __name__ == "__main__":
    init()
