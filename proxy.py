'''
    Disclaimer
    tiny httpd is a web server program for instructional purposes only
    It is not intended to be used as a production quality web server
    as it does not fully in compliance with the 
    HTTP RFC https://tools.ietf.org/html/rfc2616

'''
import socket
import sys
import mimetypes
import os
import subprocess

class HTTPServer:
    '''
        Remove the pass statement below and write your code here
    '''
    def __init__(self, localhost, port_number):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the port
        server_address = (localhost, port_number)
        print(sys.stderr, 'starting up on %s port %s' % server_address)
        sock.bind(server_address)
        
        # Listen for incoming connections
        sock.listen()
        print("Current Working Directory: "+os.getcwd())
        print("Length of the directory: "+str(len(os.getcwd())))
        
        while True:
            # Wait for a connection
            print(sys.stderr, 'waiting for a connection')
            connection, client_address = sock.accept()
            message = connection.recv(1024).decode()
            print(message)
            getmsg = message.splitlines()
            print(getmsg,"getmsg")
            cdirectory = getmsg[0].split(" ")[1]
            print(cdirectory,"cd")
            fname = cdirectory.split("/")[-1]
            print(fname,"frequest")#
             
            data_url = os.getcwd()+cdirectory
            print(data_url,"URL")
            # print(fname)
            body=""

            if(cdirectory=="/"):
                body = "<h1>Developing Web Server</h1><br>"+'\r\n'
                headers = ""
                headers += "HTTP/1.1 200 OK"+'\r\n'
                headers += "Content-Type: text/HTML "+'\r\n'
                headers += "Content-Length: %s "%str(len(body))+'\r\n'
                headers += "Connection: close "+'\r\n'
                headers += "\n"
                data = bytes(headers+body,'utf-8')
                connection.sendall(data)

            elif(os.path.isdir(data_url)):

                # if(cdirectory=="/www"):
                for files in os.listdir(cdirectory[1:]):
                    body+=f'<a href="{os.path.join(cdirectory,files)}">{files}</a><br>'
                head = f'HTTP/1.1 200 OK \nContent-Type: text/html\nContent-Length: {str(len(body))} \nConnection: close\n\n'
                print(head)
                connection.sendall((head+body).encode())
                    
                # elif(cdirectory=="/www/rough"):
                #     for file in os.listdir(cdirectory[1:]):
                #         body+=f'<a href="{os.path.join(cdirectory,file)}">{file}</a><br>'
                #     head = f'HTTP/1.1 200 OK \nContent-Type: text/html\nContent-Length: {str(len(body))} \nConnection: close\n\n'
                #     print(head)
                #     connection.sendall((head+body).encode())
                
                # elif(cdirectory=="/bin"):
                #     # for (root,dirs,files) in os.walk('bin', topdown=True):
                #     #     print (root)
                #     #     print (dirs)
                #     #     print (files)
                #     #     print ('--------------------------------')
                #     for file in os.listdir(cdirectory[1:]):
                #         body+=f'<a href="{os.path.join(cdirectory,file)}">{file}</a><br>'
                #     head = f'HTTP/1.1 200 OK \nContent-Type: text/html\nContent-Length: {str(len(body))} \nConnection: close\n\n'
                #     print(head)
                #     connection.sendall((head+body).encode())
            
            elif(cdirectory=="/bin/du"):
                # p1 = exec('du')
                # print(p1,"P1")
                output = os.popen('du','r',1)
                output_data = output.read()
                head = f'HTTP/1.1 200 OK \nContent-Type: text/plain\nContent-Length: {str(len(output_data))} \nConnection: close\n\n'
                head += output_data
                print(head,"HEAD")
                connection.sendall((head).encode())


            elif(cdirectory=="/bin/ls"):
                output = os.popen('dir','r',1)
                output_data = output.read()
                head = f'HTTP/1.1 200 OK \nContent-Type: text/plain\nContent-Length: {str(len(output_data))} \nConnection: close\n\n'
                print(head)
                connection.sendall((head+output_data).encode())

            elif(cdirectory=="/bin/test.py"):
                # p1 = exec(open(data_url,'rb').read())
                # print(p1,"SubProcess")
                output = subprocess.Popen(['python',data_url],stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
                print(output,"OUTPUT")
                out = output.communicate()[0]
                p = out.decode()
                # output = open(data_url,'rb')
                # output_data = output.read()
                # p = exec(output_data)
                # print(p,"P")
                head = f'HTTP/1.1 200 OK \nContent-Type: text/plain\nContent-Length: {str(len(p))} \nConnection: close\n\n'
                head += p
                print(head,"HEAD")
                connection.sendall((head).encode())
            
            elif(cdirectory=="/bin/rough/Sample.py"):
                output = subprocess.Popen(['python',data_url],stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
                print(output,"OUTPUT")
                out = output.communicate()[0]
                p = out.decode()
                body = f"<h1>{p}</h1><br>"+'\r\n'
                head = f'HTTP/1.1 200 OK \nContent-Type: text/HTML \nContent-Length: {str(len(body))}\nConnection: close\n\n'
                head += body
                print(head,"HEAD")
                connection.sendall((head).encode())

             # checking if it is a file        
            elif os.path.isfile(data_url):
                file = open(data_url, 'rb')
                file_data = file.read()
                file.close()
                headers = "HTTP/1.1 200 OK"+'\r\n'
                headers += f"Content-Type: {(mimetypes.MimeTypes().guess_type(fname)[0])}"+'\r\n'
                headers += "Content-Length: %s "%str(len(file_data))+'\r\n'
                headers += "Connection: close "+'\r\n'
                headers += "\n"
                headers = headers.encode()
                headers += file_data
                connection.sendall(headers)
            

            else:
                body = "<h1>404 Error</h1><br>"+'\r\n'
                body += "<h2>Page not found</h2><br>"+'\r\n'
                headers = ""
                headers += "HTTP/1.1 200 OK"+'\r\n'
                headers += "Content-Type: text/HTML "+'\r\n'
                headers += "Content-Length: %s "%str(len(body))+'\r\n'
                headers += "Connection: close "+'\r\n'
                headers += "\n"
                data = bytes(headers+body,'utf-8')
                connection.sendall(data)
                
            connection.close()


def main():
    # test harness checks for your web server on the localhost and on port 8888
    # do not change the host and port
    # you can change  the HTTPServer object if you are not following OOP
    HTTPServer('127.0.0.1', 8888)

if __name__ == "__main__":
    main()
