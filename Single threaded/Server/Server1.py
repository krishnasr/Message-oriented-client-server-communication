
import socket
import os

# the below variables are constant vairables used for coding the program
port_num=8080 # using port number 8080
server_num=socket.gethostbyname(socket.gethostname()) # gethostname returns the current computer's ip address
server_address=(server_num,port_num)
server_connected=1
message_format='utf-8'

socket_server=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #creating socket
socket_server.bind(server_address) #binding to IPV4 server hence we used AF_INET
socket_server.listen() # the server is listening to the client to receive any commands
print("the connected server "+str(server_num)+" is listening ")

class switch_process:
    def __init__(self, process):
        self.process=process

    def upload_process(self):
        filename=client_connect.recv(1024).decode(message_format) # receiving the file name to the server for upload
        curr_file=open(filename,"wb")
        curr_filedata=client_connect.recv(1024)
        flag="available"
        while flag=="available":
            curr_filedata=client_connect.recv(1024) # receiving the file data to the server
            if curr_filedata:
                curr_file.write(curr_filedata)
            else:
                flag="notavailable"           
        curr_file.close()
        print("the file "+filename+" is received")
    
    def download_process(self):
        file_path=client_connect.recv(3072).decode(message_format) #receiving the server's file path to get the list of files that are in the server
        files_list=os.listdir(file_path)
        files_list.append("cancel")
        for files in files_list:
            print(files)
            client_connect.send(files.encode(message_format)) # sending the file name that are in the server
        filename=client_connect.recv(1024).decode(message_format)
        curr_file=open(filename,"rb")
        flag="available"
        while flag=="available":
            curr_filedata=curr_file.read(1024)
            if curr_filedata:
                client_connect.send(curr_filedata) # sending the file data to the client to download
            else:
                flag="notavailable"
        curr_file.close()
        print("the file "+filename+" is sent to client")
    
    def delete_process(self):
        file_path=client_connect.recv(3072).decode(message_format) #receiving the server's file path to get the list of files that are in the server
        files_list=os.listdir(file_path)
        files_list.append("cancel")
        for files in files_list:
            print(files)
            client_connect.send(files.encode(message_format)) # sending the file name that are in the server
        filename=client_connect.recv(1024).decode(message_format) # receiving the filename that need to be deleted
        os.remove(filename)
        print("the file "+filename+" is deleted ")

    def rename_process(self):
        file_path=client_connect.recv(3072).decode(message_format) #receiving the server's file path to get the list of files that are in the server
        files_list=os.listdir(file_path)
        files_list.append("cancel")
        for files in files_list:
            print(files)
            client_connect.send(files.encode(message_format)) # sending the file name that are in the server
        filename=client_connect.recv(1024).decode(message_format) # receiving the filename that need to be renamed
        file_newname=client_connect.recv(1024).decode(message_format) # receiving new file name
        os.rename(filename,file_newname)
        print(" the file "+filename+" is renamed to "+ file_newname)
        files_list=os.listdir(file_path)
        files_list.append("cancel")
        for files in files_list:
            print(files)
            client_connect.send(files.encode(message_format))


while server_connected==1:
    client_connect,client_address=socket_server.accept()
    client_message=client_connect.recv(1024).decode(message_format) # the server receives the message from the client to do the type of process
    print("Current process running in server: "+str(client_message))

    if client_message=="Upload": # this condition does UPLOAD process
        process_switch=switch_process("Upload")
        process_switch.upload_process() 
        break
        
    elif client_message=="Download": # this condition does DOWNLOAD process
        process_switch=switch_process("Download")
        process_switch.download_process() 
        break
    
    elif client_message=="Delete": # this condition does DELETE process
        process_switch=switch_process("Delete")
        process_switch.delete_process() 
        break
    elif client_message=="Rename": # this condition does RENAME process
        process_switch=switch_process("Rename")
        process_switch.rename_process() 
        break

client_connect.close()


