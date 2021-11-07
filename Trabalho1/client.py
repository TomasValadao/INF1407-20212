from sys import argv, stderr
from socket import getaddrinfo, socket
from socket import AF_INET, SOCK_STREAM, IPPROTO_TCP, AI_ADDRCONFIG
from os import abort

def getEnderecoServidor(host, porta):
    try:
        enderecoServidor = getaddrinfo(host,
                                       porta,
                                       family=AF_INET,
                                       type=SOCK_STREAM,
                                       proto=IPPROTO_TCP,
                                       flags=AI_ADDRCONFIG)
    except:
        print("Não obtive informações sobre servidor", file=stderr)
        abort()
        
    return enderecoServidor

def criaSocket(enderecoServidor):
    fd = socket(enderecoServidor[0][0], enderecoServidor[0][1])
    if not fd:
        print("Não consegui criar o socket")
        abort()
        
    return fd

def conecta(socketfd, enderecoServidor):
    try:
        socketfd.connect(enderecoServidor[0][4])
    except:
        print("Erro ao tentar conexão com o servidor",
              enderecoServidor[0][4],
              file=stderr)
        abort()
    return

def fazOResto(fd):
    test = "GET /Examples/script.js HTTP/1.1\r\n\r\n"
    fd.send(bytearray(test, 'utf-8'))

    while True:
        bufferEntrada = fd.recv(1024)
        print("==>", bufferEntrada)
        
        if not bufferEntrada:
            break
    return

def main():
    host = 'localhost'
    porta = 8080   
    
    enderecoServidor = getEnderecoServidor(host, porta)
    socketfd = criaSocket(enderecoServidor)
    conecta(socketfd, enderecoServidor)
    fazOResto(socketfd)
    socketfd.close()
    return


if __name__ == '__main__':
    main()
