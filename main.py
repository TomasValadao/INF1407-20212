import config as CONFIG
from datetime import datetime
from os import abort, chdir, fork, getcwd, listdir
from socket import socket, getaddrinfo
from socket import AF_INET, SOCK_STREAM, IPPROTO_TCP, AI_ADDRCONFIG, AI_PASSIVE, SOL_SOCKET, SO_REUSEADDR

class WebServer:
    
    def __init__(self, port, pathToFilesDir, notFoundHandler):
        self.port = port
        self.pathToFilesDir = pathToFilesDir
        self.notFoundHandler = notFoundHandler
        
        self.__hostAddress = None
        self.__socket = None
        return
    
    def __setHostAddress(self):
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
            print("Failed to set host address for our WebServer!")
            abort()
            
        return
    
    def __setSocket(self):
        self.__socket = socket(self.__hostAddress[0][0], self.__hostAddress[0][1])

        if self.__socket is None:
            print('Failed to create socket for our WebServer!')
            abort()
        
        self.__socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        
        return
    
    def __bindSocket(self):
        try:
            self.__socket.bind(('', self.port))
    
        except:
            print('Failed to bind socket for our WebServer!')
            abort()
    
        return
    
    def __enableConnectionAcceptance(self):
        try:
            self.__socket.listen(8)
    
        except:
            print('Failed to initialize socket!')
            abort()
    
        return
    
    def __acceptConnection(self):
        (connection, client) = self.__socket.accept()
        print('Server is connected with %s!' % client[0])
    
        return (connection, client)
    
    def getFileResponseType(self, file):
        types = {
            "png": "image/png",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "gif": "image/gif",
            "html": "text/html",
            "js": "application/javascript"
            }
        
        return types.get(file.split(".")[-1], None)
        
    def getFilePath(self, file):
        return getcwd().replace("\\", "/") + file
    
    def hasRequestedFile(self, file):
        fullRequestedFile = self.getFilePath(file)
        
        chdir(self.pathToFilesDir)
        
        for dirFile in listdir():
            formattedDirFile = getcwd().replace("\\", "/") + "/" + dirFile
            
            if formattedDirFile == fullRequestedFile:
                chdir("..")
                return True
            
        chdir("..")    
        return False

    def handleRequest(self, connection):
        while True:
            message = connection.recv(1024)
            
            if not message:
                break
            
            parsedMessage = message.decode("utf-8").split("\r\n")
            
            if parsedMessage is None:
                break

            requestedPath = parsedMessage[0].split(" ")
            
            if len(requestedPath) < 3:
                print("Incorrect Get Request Path")
                break
            
            filePath = requestedPath[1]
            
            if self.hasRequestedFile(filePath):
                print("Requested file was found!")
                
                file = open(self.getFilePath(filePath), 'rb')
                content = file.read()
                fileByteArray =  bytearray(content)
                statusCode = "HTTP/1.1 200 OK\r\n"
                
                fileContentType = self.getFileResponseType(filePath)
                
                if fileContentType == None:
                    break

                fileType = "Content-Type: %s\r\n" % fileContentType
                
            else:
                print("Requested file was not found!")
                
                file = open(self.getFilePath(self.notFoundHandler), 'rb')
                content = file.read()
                fileByteArray =  bytearray(content)
                statusCode = "HTTP/1.1 404 NOT FOUND\n\n"
                fileType = "Content-Type: text/html\n"
            
            connection.sendall(bytearray(statusCode, "utf-8"))
            connection.sendall(bytearray("Server: Apache-Coyote/1.1\n", "utf-8"))
            connection.sendall(bytearray(fileType, "utf-8"))
            connection.sendall(bytearray("Content-Length: %d\n" % len(fileByteArray), "utf-8"))
            connection.sendall(bytearray("Date: %s\n" % datetime.now().ctime(), "utf-8"))
            connection.sendall(content)

        connection.close()  
        exit()

        return

    def runServer(self):
        self.__setHostAddress()
        self.__setSocket()
        self.__bindSocket()
        self.__enableConnectionAcceptance()
        
        print("Server was fully configured! It is now running on PORT %d" % self.port)
        
        while True:
            connection, client = self.__acceptConnection()
            print("Server connected with %s" % client[0])

            pid = fork()
    
            if pid == 0:
                self.handleRequest(self.__socket, connection)
                print("Connection closed with %s" % client[0])
    
            else:
                connection.close()
                print("Connection closed with %s" % client[0])
        return

if __name__ == "__main__":
    server = WebServer(CONFIG.PORT, CONFIG.EXTENDED_PATH_TO_FILES, CONFIG.PATH_TO_404)
    server.runServer()