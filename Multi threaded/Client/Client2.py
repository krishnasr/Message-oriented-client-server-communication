from asyncio.windows_events import NULL
import socket
import os

# the below variables are constant vairables used for coding the program
port_num=8080 # server port number 8080
server_num=socket.gethostbyname(socket.gethostname()) # gethostname returns the current computer's ip address
server_address=(server_num,port_num)
message_format='utf-8'
infinite_loop="infinite"
socket_server=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #creating socket
socket_server.bind((server_num,5051))
socket_server.connect(server_address) #connecting to IPV4 server hence we used AF_INET

class switch_process:
    def __init__(self, process):
        self.process=process

    def upload_process(self):
        filename=input("please enter the file name: ")
        filename_send=filename.encode(message_format)
        socket_server.send(filename_send) # sending the file name to the server for upload
        curr_file=open(filename,"rb")
        flag="available"
        while flag=="available":
            curr_filedata=curr_file.read(1024)
            if curr_filedata:
                socket_server.send(curr_filedata) # sending the file data to the server
            else:
                flag="notavailable"     
        curr_file.close()
        print("the File "+filename+" is Uploaded")


    def download_process(self):
        file_path=input("enter the file path to list the files ") 
        file_pathsend=file_path.encode(message_format) #sending the server's file path to get the list of files that are in the server
        socket_server.send(file_pathsend)
        files_list=socket_server.recv(1024).decode(message_format)
        while files_list!="cancel":
            print(files_list) # the file list are printed
            files_list=socket_server.recv(1024).decode(message_format)
        
        file_selected=input("Please select a file and enter the file name to download ")
        file_selectedsend=file_selected.encode(message_format) # sending the filename that need to be downloaded
        socket_server.send(file_selectedsend)
        curr_file=open(file_selected,"wb")
        flag="available" 
        while flag=="available" :
            curr_filedata=socket_server.recv(1024)
            if curr_filedata:
                curr_file.write(curr_filedata) # here we are downloading the file by writing it
            else:
                flag="notavailable" 
        curr_file.close()
        print("the file "+file_selected+" is Downloaded")
    

    def delete_process(self):
        file_path=input("enter the file path to list the files ")
        file_pathsend=file_path.encode(message_format) #sending the server's file path to get the list of files that are in the server
        socket_server.send(file_pathsend)
        files_list=socket_server.recv(1024).decode(message_format)
        while files_list!="cancel":
            print(files_list) # the file list are printed
            files_list=socket_server.recv(1024).decode(message_format)
        file_selected=input("Please select a file and enter the file name to delete ") # sending the filename that need to be deleted
        file_selectedsend=file_selected.encode(message_format)
        socket_server.send(file_selectedsend)
        print(" the file "+file_selected+" is deleted in the server")

    def rename_process(self):
        file_path=input("enter the file path to list the files ") 
        file_pathsend=file_path.encode(message_format) #sending the server's file path to get the list of files that are in the server
        socket_server.send(file_pathsend)
        files_list=socket_server.recv(1024).decode(message_format)
        while files_list!="cancel":
            print(files_list) # the file list are printed
            files_list=socket_server.recv(1024).decode(message_format)
        file_selected=input("Please select a file and enter the file name to rename ")
        file_selectedsend=file_selected.encode(message_format)
        socket_server.send(file_selectedsend) # sending the filename that need to be renamed
        file_rename=input("Please enter the new name ")
        file_renamesend=file_rename.encode(message_format)
        socket_server.send(file_renamesend)  # sending a new name 
        newfiles_list=socket_server.recv(1024).decode(message_format)
        while newfiles_list!="cancel":
            print(newfiles_list) # the file list are printed after renameing 
            newfiles_list=socket_server.recv(1024).decode(message_format)
        print(" the file "+file_selected+" is renamed to "+ file_rename)


print(" The process are Upload, Download, Rename, Delete select a process ")
process=input("Please enter the type of process ")
process_send=process.encode(message_format) #sending the type of process to the server
socket_server.send(process_send)
curr_process=process  
if curr_process=="Upload": # this condition does UPLOAD process
    process_switch=switch_process("Upload")
    process_switch.upload_process()

elif curr_process=="Download": # this condition does DOWNLOAD process
    process_switch=switch_process("Download")
    process_switch.download_process()

elif curr_process=="Delete": # this condition does DELETE process
    process_switch=switch_process("Delete")
    process_switch.delete_process()

elif curr_process=="Rename": # this condition does RENAME process
    process_switch=switch_process("Rename")
    process_switch.rename_process()








