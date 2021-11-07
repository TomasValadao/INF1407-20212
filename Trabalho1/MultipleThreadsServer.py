import config as CONFIG
from datetime import datetime
from os import abort, chdir, getcwd, listdir, path
from socket import socket, getaddrinfo
from socket import AF_INET, SOCK_STREAM, IPPROTO_TCP, AI_ADDRCONFIG, AI_PASSIVE, SOL_SOCKET, SO_REUSEADDR
from time import sleep
from _thread import start_new_thread
import threading

server_lock = threading.Lock()

class WebServer:
    
    def __init__(self, port, pathToFilesDir, defaultFiles, notFoundHandler):
        self.port = port
        self.pathToFilesDir = pathToFilesDir
        self.defaultFiles = defaultFiles
        self.notFoundHandler = notFoundHandler
        
        self.__hostAddress = None
        self.__socket = None
        return
    
    # Método com o intuito de ser Private.
    def __setHostAddress(self):
        # Tenta setar gerar as informações do Host Address
        # E tenta dar um bind no objeto da Classe WebServer.
        
        try:
            self.__hostAddress = getaddrinfo(
                None,
                self.port,
                AF_INET,
                SOCK_STREAM,
                IPPROTO_TCP,
                AI_ADDRCONFIG | AI_PASSIVE
            )
    
        except:
            print("Failed to set host address for our WebServer!\n")
            abort()
            
        return
    
    # Método com o intuito de ser Private.
    def __setSocket(self):
        # Instancia um objeto do tipo Socket e atualiza o campo __socket do Objeto WebServer.
        self.__socket = socket(self.__hostAddress[0][0], self.__hostAddress[0][1])

        if self.__socket is None:
            print('Failed to create socket for our WebServer!\n')
            abort()
        
        # Configura o Socket pra reutilizar socket antigos que foram vinculados ao mesmo Address
        self.__socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        
        return
    
    # Método com o intuito de ser Private.
    def __bindSocket(self):
        # Associa o endereço e uma porta ao Socket
        try:
            self.__socket.bind(('', self.port))
    
        except:
            print('Failed to bind socket for our WebServer!\n')
            abort()
    
        return
    
    # Método com o intuito de ser Private.
    def __enableConnectionAcceptance(self):
        # Permite com que o socket aceite o recebimento de conexões e seu limite.
        try:
            self.__socket.listen(0)
    
        except:
            print('Failed to initialize socket!\n')
            abort()
    
        return
    
    # Método com o intuito de ser Private.
    def __acceptConnection(self):
        # O Socket aceita uma conexão de um dado cliente.
        (connection, client) = self.__socket.accept()
        print('Server is connected with %s!\n' % client[0])
    
        return (connection, client)
    
    # Método com o intuito de ser Public.
    def getFileResponseType(self, file):
        # Decide o tipo de CONTENT-TYPE, caso esteja mapeado.
        
        types = {
            "png": "image/png",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "gif": "image/gif",
            "html": "text/html",
            "js": "application/javascript"
            }
        
        return types.get(file.split(".")[-1], None)
    
    # Método com o intuito de ser Public.
    def getFilePath(self, file):
        # Pega o Path inteiro do Arquivo.
        return getcwd().replace("\\", "/") + file
    
    # Método com o intuito de ser Public.
    def hasRequestedFile(self, file):
        # Decide se o File existe na pasta contida no attr pathToFilesDir
        fullRequestedFile = self.getFilePath(file)
        
        chdir(self.pathToFilesDir)
        
        for dirFile in listdir():
            formattedDirFile = getcwd().replace("\\", "/") + "/" + dirFile
            
            if formattedDirFile == fullRequestedFile:
                chdir("..")
                return True
            
        chdir("..")    
        return False

    # Método com o intuito de ser Public.
    def handleRequest(self, connection):
        canBreakLoop = False
        
        while True:
            if canBreakLoop:
                break
            
            message = connection.recv(1024)

            if not message:
                break
            
            decodedMessage = message.decode("utf-8")
            
            # Decide se o recv retorno o final da stream de dados.
            if decodedMessage[-4:] == "\r\n\r\n":
                canBreakLoop = True

            parsedMessage = decodedMessage.split("\r\n")
            
            # Verifica se o parse estava incompleto.
            if not parsedMessage:
                break

            requestedPath = parsedMessage[0].split(" ")
            
            # Verifica se o GET Request está errado.
            if len(requestedPath) < 3:
                print("Incorrect Get Request Path\n")
                break
            
            filePath = requestedPath[1]
            
            # Procura pelo arquivo desejado
            if self.hasRequestedFile(filePath):
                print(f"Requested file {filePath} was found!\n")
                
                fullFilePath = self.getFilePath(filePath)
                statusCode = "HTTP/1.1 200 OK\r\n"
                
            else:
                print(f"Requested file {filePath} was not found!\n")
                statusCode = "HTTP/1.1 404 NOT FOUND\r\n"

                # Procura pela Lista default de arquivos
                if filePath == '/':
                    print("Trying to get default file...\n")
                    fullFilePath = self.getFilePath(self.notFoundHandler)
                    
                    for defaultFile in self.defaultFiles:
                        if self.hasRequestedFile(defaultFile):
                            fullFilePath = self.getFilePath(defaultFile)
                            statusCode = "HTTP/1.1 200 OK\r\n"
                            break
                # Utiliza o arquivo 404
                else:
                    fullFilePath = self.getFilePath(self.notFoundHandler)
                
                
            file = open(fullFilePath, 'rb')
            content = file.read()
            byteArrayLength = path.getsize(fullFilePath)
            fileContentType = self.getFileResponseType(fullFilePath)
            
            if fileContentType == None:
                break
            
            fileType = "Content-Type: %s\r\n" % fileContentType
            
            # Monta e Envia o Response com o arquivo escolhido (ou não encontrado)!
            connection.sendall(bytearray(statusCode, "utf-8"))
            connection.sendall(bytearray("Server: Apache-Coyote/1.1\r\n", "utf-8"))
            connection.sendall(bytearray(fileType, "utf-8"))
            connection.sendall(bytearray("Content-Length: %d\r\n" % byteArrayLength, "utf-8"))
            connection.sendall(bytearray("Date: %s\r\n\r\n" % datetime.now().ctime(), "utf-8"))
            connection.sendall(content)

        # Encerra a Thread e fecha a conexão com o cliente!
        server_lock.release()
        connection.close()
        exit()
        
        return

    # Método com o intuito de ser Public.
    def runServer(self):
        # Essa função tem como objetivo configurar a socket com as informações do config.py
        # E num loop "infinito", o socket deverá aceitar as requisições GET de um cliente
        # Para fazer o uso do paralelismo, é aberto uma thread pra chamar o método handleRequest do objeto
        
        self.__setHostAddress()
        self.__setSocket()
        self.__bindSocket()
        self.__enableConnectionAcceptance()
        
        print("Server was fully configured! It is now running on PORT %d\n" % self.port)
        
        while True:
            connection, client = self.__acceptConnection()
            print("Server connected with %s\n" % client[0])
            
            # Da locked no Lock global
            server_lock.acquire()
            sleep(2)
            # Inicia a execução do Handle Request!
            start_new_thread(self.handleRequest, (connection,))
            
        connection.close()
        print("Connection closed with %s\n" % client[0])
        return

if __name__ == "__main__":
    server = WebServer(CONFIG.PORT, CONFIG.EXTENDED_PATH_TO_FILES, CONFIG.DEFAULT_FILES, CONFIG.PATH_TO_404)
    server.runServer()
